"""
Tom Gair Portfolio - FastAPI Backend
A clean, professional portfolio site with admin functionality.
Built with FastAPI, Jinja2, HTMX, and Tailwind CSS.
"""
import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Request, Form, HTTPException, Header, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Tom Gair — Python/FastAPI Developer")

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
VISITS_FILE = DATA_DIR / "visits.json"

# Initialize projects file if it doesn't exist
if not PROJECTS_FILE.exists():
    with open(PROJECTS_FILE, "w") as f:
        json.dump([], f)

# Initialize contacts file if it doesn't exist
if not CONTACTS_FILE.exists():
    with open(CONTACTS_FILE, "w") as f:
        json.dump([], f)

# Initialize visits file
if not VISITS_FILE.exists():
    with open(VISITS_FILE, "w") as f:
        json.dump({"home": 0}, f)


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
    """Load blog posts with frontmatter from content/blog/*.md.
    Frontmatter keys: title, date, summary, tags (comma-separated or YAML list).
    """
    blog_dir = Path("content/blog")
    blog_dir.mkdir(parents=True, exist_ok=True)

    posts = []
    for md_file in blog_dir.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            raw = f.read()
        fm = {}
        body = raw
        if raw.startswith("---"):
            parts = raw.split("\n", 1)[1].split("\n---\n", 1)
            if len(parts) == 2:
                # Parse simple YAML-like frontmatter without external deps
                raw_fm, body = parts
                for line in raw_fm.splitlines():
                    if not line.strip() or ":" not in line:
                        continue
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
                # tags may be comma-separated
                if "tags" in fm and isinstance(fm["tags"], str):
                    fm["tags"] = [t.strip() for t in fm["tags"].split(",") if t.strip()]
        title = fm.get("title") or md_file.stem.replace("-", " ").title()
        date = fm.get("date") or datetime.fromtimestamp(md_file.stat().st_mtime).strftime("%Y-%m-%d")
        summary = fm.get("summary") or ""
        tags = fm.get("tags") or []
        posts.append({
            "slug": md_file.stem,
            "title": title,
            "date": date,
            "summary": summary,
            "tags": tags,
            "content": body,
        })
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts

# Simple visit counter helpers
def increment_visit(key: str) -> int:
    try:
        with open(VISITS_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data[key] = int(data.get(key, 0)) + 1
    with open(VISITS_FILE, "w") as f:
        json.dump(data, f)
    return data[key]

def get_visit_count(key: str) -> int:
    try:
        with open(VISITS_FILE, "r") as f:
            data = json.load(f)
        return int(data.get(key, 0))
    except Exception:
        return 0


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """Robots.txt allowing public site, disallowing admin, with sitemap."""
    return """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /admin-login
Disallow: /admin-logout
Sitemap: /sitemap.xml"""

@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap_xml():
    base = "https://gair.dev"  # adjust if hosted elsewhere
    urls = ["/", "/projects", "/blog", "/resume", "/contact"]
    # include project slugs
    for p in load_projects():
        if p.get("slug"):
            urls.append(f"/projects/{p['slug']}")
    # include blog slugs
    for b in load_blog_posts():
        urls.append(f"/blog/{b['slug']}")
    items = "".join([f"<url><loc>{base}{u}</loc></url>" for u in urls])
    return PlainTextResponse(content=f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">{items}</urlset>", media_type="application/xml")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with simple visit counter (no cookies)."""
    count = increment_visit("home")
    return templates.TemplateResponse("home.html", {
        "request": request,
        "title": "Home",
        "visit_count": count,
    })


@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    """Projects page with tag filters (HTMX) and list."""
    projects = load_projects()
    tags = sorted({t for p in projects for t in p.get("tags", [])})
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "title": "Projects",
        "projects": projects,
        "all_tags": tags,
        "current_tag": None,
    })

@app.get("/projects/filter", response_class=HTMLResponse)
async def projects_filter(request: Request, tag: Optional[str] = None):
    """Return filtered project list fragment for HTMX."""
    projects = load_projects()
    if tag:
        projects = [p for p in projects if tag in p.get("tags", [])]
    # Render only the list items
    # Use a minimal container to allow innerHTML swap
    items_html = []
    for p in projects:
        items_html.append(templates.get_template("project_item.html").render({"request": request, "project": p}))
    return HTMLResponse("\n".join(items_html))

@app.get("/projects/{slug}", response_class=HTMLResponse)
async def project_detail(request: Request, slug: str):
    """Project case study page."""
    projects = load_projects()
    proj = next((p for p in projects if p.get("slug") == slug), None)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("project_detail.html", {
        "request": request,
        "title": proj.get("title", "Project"),
        "project": proj,
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
    
    # Add new project (conform to new schema used by templates)
    slug = "proj-" + secrets.token_urlsafe(6).lower().replace("_", "-")
    new_project = {
        "id": (max([p.get("id", 0) for p in projects]) + 1) if projects else 1,
        "slug": slug,
        "title": name,
        "summary": description,
        "tags": [],
        "stack": [],
        "badges": [],
        "links": {"repo": None, "demo": None, "site": None},
        "created_at": datetime.now().isoformat()
    }
    if url:
        # Heuristic: store under repo if GitHub-like, else demo
        if "github.com" in url:
            new_project["links"]["repo"] = url
        else:
            new_project["links"]["demo"] = url
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
        "post": {"title": post["title"], "created_at": post.get("date", ""), "slug": post["slug"]},
        "html_content": html_content
    })


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact page: short copy with mailto and GitHub link."""
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "title": "Contact"
    })

@app.get("/resume", response_class=HTMLResponse)
async def resume_page(request: Request):
    return templates.TemplateResponse("resume.html", {
        "request": request,
        "title": "Resume"
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
    blog_posts = load_blog_posts()
    
    csrf_token = generate_csrf_token()
    
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "title": "Admin Dashboard",
        "projects": projects,
        "contacts": contacts,
        "blog_posts": blog_posts,
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


@app.post("/admin/blog/create")
async def admin_create_blog_post(
    title: str = Form(...),
    content: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    csrf_token: str = Form(...),
    session_id: Optional[str] = Cookie(None)
):
    """Create a new blog post (admin only)."""
    # Verify session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Verify CSRF token
    if not verify_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    # Generate slug if not provided
    if not slug:
        slug = title.lower().replace(" ", "-")
        # Remove special characters and clean up
        import re
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
    
    # Parse tags
    tag_list = []
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    # Create frontmatter content
    frontmatter_lines = [
        "---",
        f"title: {title}",
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
    ]
    
    if summary:
        frontmatter_lines.append(f"summary: {summary}")
    
    if tag_list:
        frontmatter_lines.append(f"tags: {', '.join(tag_list)}")
    
    frontmatter_lines.append("---")
    
    # Combine frontmatter and content
    full_content = "\n".join(frontmatter_lines) + "\n\n" + content
    
    # Ensure content/blog directory exists
    blog_dir = Path("content/blog")
    blog_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the blog post file
    blog_file = blog_dir / f"{slug}.md"
    
    # Check if file already exists
    if blog_file.exists():
        raise HTTPException(status_code=400, detail=f"Blog post with slug '{slug}' already exists")
    
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(full_content)
    
    return RedirectResponse(url="/admin", status_code=302)


@app.post("/admin/blog/delete/{slug}")
async def admin_delete_blog_post(
    slug: str,
    csrf_token: str = Form(...),
    session_id: Optional[str] = Cookie(None)
):
    """Delete a blog post (admin only)."""
    # Verify session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Verify CSRF token
    if not verify_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    # Delete the blog post file
    blog_file = Path("content/blog") / f"{slug}.md"
    
    if not blog_file.exists():
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    blog_file.unlink()
    
    return RedirectResponse(url="/admin", status_code=302)


@app.post("/admin/projects/create")
async def admin_create_project(
    title: str = Form(...),
    summary: str = Form(...),
    slug: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    stack: Optional[str] = Form(None),
    repo_url: Optional[str] = Form(None),
    demo_url: Optional[str] = Form(None),
    site_url: Optional[str] = Form(None),
    csrf_token: str = Form(...),
    session_id: Optional[str] = Cookie(None)
):
    """Create a new project (admin only)."""
    # Verify session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Verify CSRF token
    if not verify_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    # Load existing projects
    projects = load_projects()
    
    # Generate slug if not provided
    if not slug:
        slug = title.lower().replace(" ", "-")
        # Remove special characters and clean up
        import re
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
    
    # Parse tags and stack
    tag_list = []
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    stack_list = []
    if stack:
        stack_list = [tech.strip() for tech in stack.split(",") if tech.strip()]
    
    # Create new project
    new_project = {
        "id": (max([p.get("id", 0) for p in projects]) + 1) if projects else 1,
        "slug": slug,
        "title": title,
        "summary": summary,
        "tags": tag_list,
        "stack": stack_list,
        "badges": [],
        "links": {
            "repo": repo_url if repo_url else None,
            "demo": demo_url if demo_url else None,
            "site": site_url if site_url else None
        },
        "created_at": datetime.now().isoformat()
    }
    
    # Add to projects list
    projects.append(new_project)
    
    # Save projects
    save_projects(projects)
    
    return RedirectResponse(url="/admin", status_code=302)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

# Health endpoint for uptime checks and tests
@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})

# --- JSON -> SQLite upgrade path (SQLModel stub) ---
# from sqlmodel import SQLModel, Field
# class Project(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     slug: str
#     title: str
#     summary: str
#     tags: list[str] | None = None  # could be normalized to a tags table
#     created_at: datetime | None = None
#     # JSON columns could be split across normalized tables in real schema
