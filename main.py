import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Request, Form, HTTPException, Header, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
from dotenv import load_dotenv
import secrets
import hashlib
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Tom Gair's Portfolio")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Admin credentials from environment
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me-in-production")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-me-in-production")

# Session storage (in-memory, would use Redis in production)
sessions = {}
CSRF_TOKENS = {}

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


def create_session(username: str) -> str:
    """Create a new session for the user."""
    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = {
        "username": username,
        "created_at": datetime.now().isoformat()
    }
    return session_id


def get_session(session_id: Optional[str]) -> Optional[dict]:
    """Get session data by session ID."""
    if not session_id:
        return None
    return sessions.get(session_id)


def generate_csrf_token() -> str:
    """Generate a CSRF token."""
    token = secrets.token_urlsafe(32)
    CSRF_TOKENS[token] = datetime.now()
    return token


def verify_csrf_token(token: str) -> bool:
    """Verify CSRF token is valid."""
    if token in CSRF_TOKENS:
        # Token is valid, remove it (one-time use)
        del CSRF_TOKENS[token]
        return True
    return False


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


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """Robots.txt to disallow admin crawling."""
    return """User-agent: *
Disallow: /admin/
Disallow: /admin-login
Disallow: /admin-logout"""


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


@app.get("/admin-login", response_class=HTMLResponse)
async def admin_login_page(request: Request, session_id: Optional[str] = Cookie(None)):
    """Admin login page."""
    # Check if already logged in
    session = get_session(session_id)
    if session:
        return RedirectResponse(url="/admin", status_code=302)
    
    csrf_token = generate_csrf_token()
    return templates.TemplateResponse("admin_login.html", {
        "request": request,
        "title": "Admin Login",
        "csrf_token": csrf_token
    })


@app.post("/admin-login", response_class=HTMLResponse)
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...)
):
    """Handle admin login."""
    # Verify CSRF token
    if not verify_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    # Verify credentials
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Create session
        session_id = create_session(username)
        
        # Redirect to admin dashboard
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=86400,  # 24 hours
            samesite="strict"
        )
        return response
    else:
        # Invalid credentials
        csrf_token = generate_csrf_token()
        return templates.TemplateResponse("admin_login.html", {
            "request": request,
            "title": "Admin Login",
            "csrf_token": csrf_token,
            "error": "Invalid username or password"
        })


@app.get("/admin-logout")
async def admin_logout(session_id: Optional[str] = Cookie(None)):
    """Logout admin."""
    if session_id and session_id in sessions:
        del sessions[session_id]
    
    response = RedirectResponse(url="/admin-login", status_code=302)
    response.delete_cookie("session_id")
    return response


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, session_id: Optional[str] = Cookie(None)):
    """Admin dashboard."""
    # Verify session
    session = get_session(session_id)
    if not session:
        return RedirectResponse(url="/admin-login", status_code=302)
    
    # Load data
    projects = load_projects()
    contacts = load_contacts()
    
    csrf_token = generate_csrf_token()
    
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "title": "Admin Dashboard",
        "projects": projects,
        "contacts": contacts,
        "csrf_token": csrf_token,
        "username": session["username"]
    })


@app.post("/admin/delete-project/{project_id}")
async def admin_delete_project(
    project_id: int,
    csrf_token: str = Form(...),
    session_id: Optional[str] = Cookie(None)
):
    """Delete a project (admin only)."""
    # Verify session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Verify CSRF token
    if not verify_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    # Delete project
    projects = load_projects()
    projects = [p for p in projects if p["id"] != project_id]
    save_projects(projects)
    
    return RedirectResponse(url="/admin", status_code=302)


@app.post("/admin/delete-contact/{contact_id}")
async def admin_delete_contact(
    contact_id: int,
    csrf_token: str = Form(...),
    session_id: Optional[str] = Cookie(None)
):
    """Delete a contact (admin only)."""
    # Verify session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Verify CSRF token
    if not verify_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    # Delete contact
    contacts = load_contacts()
    contacts = [c for c in contacts if c["id"] != contact_id]
    save_contacts(contacts)
    
    return RedirectResponse(url="/admin", status_code=302)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
