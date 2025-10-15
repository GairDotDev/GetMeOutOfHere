import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Request, Form, HTTPException, Header
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Tom Gair's Portfolio")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Admin token from environment
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me-in-production")

# Data file paths
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
PROJECTS_FILE = DATA_DIR / "projects.json"
CONTACTS_FILE = DATA_DIR / "contacts.json"

# Initialize projects file if it doesn't exist
if not PROJECTS_FILE.exists():
    with open(PROJECTS_FILE, "w") as f:
        json.dump([], f)

# Initialize contacts file if it doesn't exist
if not CONTACTS_FILE.exists():
    with open(CONTACTS_FILE, "w") as f:
        json.dump([], f)


def load_projects():
    """Load projects from JSON file."""
    try:
        with open(PROJECTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_projects(projects):
    """Save projects to JSON file."""
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=2)


def load_contacts():
    """Load contacts from JSON file."""
    try:
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_contacts(contacts):
    """Save contacts to JSON file."""
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)


def verify_admin_token(authorization: Optional[str] = Header(None)):
    """Verify admin token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return True


def load_blog_posts():
    """Load blog posts from markdown files."""
    blog_dir = Path("blog_posts")
    blog_dir.mkdir(exist_ok=True)
    
    posts = []
    for md_file in blog_dir.glob("*.md"):
        with open(md_file, "r") as f:
            content = f.read()
            # Extract title from first line if it's a heading
            lines = content.split("\n")
            title = lines[0].replace("#", "").strip() if lines else md_file.stem
            
            posts.append({
                "slug": md_file.stem,
                "title": title,
                "content": content,
                "created_at": datetime.fromtimestamp(md_file.stat().st_mtime).strftime("%Y-%m-%d")
            })
    
    # Sort by creation time (newest first)
    posts.sort(key=lambda x: x["created_at"], reverse=True)
    return posts


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("home.html", {
        "request": request,
        "title": "Home"
    })


@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    """Projects page with list and form to add new projects."""
    projects = load_projects()
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "title": "Projects",
        "projects": projects
    })


@app.post("/projects", response_class=HTMLResponse)
async def add_project(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    url: Optional[str] = Form(None),
    authorization: Optional[str] = Header(None)
):
    """Add a new project (requires admin authentication)."""
    # Verify admin token
    verify_admin_token(authorization)
    
    # Load existing projects
    projects = load_projects()
    
    # Add new project
    new_project = {
        "id": len(projects) + 1,
        "name": name,
        "description": description,
        "url": url,
        "created_at": datetime.now().isoformat()
    }
    projects.append(new_project)
    
    # Save projects
    save_projects(projects)
    
    # Return HTML fragment with the new project (for HTMX)
    return templates.TemplateResponse("project_item.html", {
        "request": request,
        "project": new_project
    })


@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    """Blog page listing all posts."""
    posts = load_blog_posts()
    return templates.TemplateResponse("blog.html", {
        "request": request,
        "title": "Blog",
        "posts": posts
    })


@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    """Individual blog post page."""
    posts = load_blog_posts()
    post = next((p for p in posts if p["slug"] == slug), None)
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Convert markdown to HTML
    html_content = markdown.markdown(post["content"], extensions=["fenced_code", "tables"])
    
    return templates.TemplateResponse("blog_post.html", {
        "request": request,
        "title": post["title"],
        "post": post,
        "html_content": html_content
    })


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact page with form."""
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "title": "Contact"
    })


@app.post("/contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    inquiry_type: str = Form(...),
    message: str = Form(...),
    company: Optional[str] = Form(None)
):
    """Handle contact form submission."""
    # Load existing contacts
    contacts = load_contacts()
    
    # Add new contact
    new_contact = {
        "id": len(contacts) + 1,
        "name": name,
        "email": email,
        "inquiry_type": inquiry_type,
        "company": company,
        "message": message,
        "submitted_at": datetime.now().isoformat()
    }
    contacts.append(new_contact)
    
    # Save contacts
    save_contacts(contacts)
    
    # Return success response (empty HTML for HTMX)
    return HTMLResponse(content="", status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
