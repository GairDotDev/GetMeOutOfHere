# Tom Gair's Portfolio

A modern portfolio website built with FastAPI, Jinja2, HTMX, and Tailwind CSS.

## Overview

This portfolio showcases my work as a backend developer, emphasizing Python/FastAPI expertise and growing SQL skills. The site features:

- **Home Page**: Introduction and skills overview
- **Projects Page**: Dynamic project showcase with HTMX-powered form to add new projects (admin-authenticated)
- **Blog**: Markdown-based blog posts for sharing thoughts and updates
- **Modern Stack**: FastAPI backend, Jinja2 templates, HTMX for interactivity, Tailwind CSS for styling

## Features

### Current Implementation
- ✅ FastAPI backend with Jinja2 template rendering
- ✅ HTMX for dynamic, no-reload form submissions
- ✅ Tailwind CSS via CDN for responsive design
- ✅ Admin token authentication for adding projects
- ✅ JSON-based project storage
- ✅ Markdown blog post support
- ✅ Clean, professional UI with navigation

### Planned Upgrades
- 🔄 **SQLite Database Migration**: Moving from JSON to SQLite for better data management
- 🔄 Additional admin features (edit/delete projects)
- 🔄 Blog post categories and tags
- 🔄 Search functionality

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GairDotDev/portfolio.git
   cd portfolio
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your admin credentials (all are required for admin login):
   ADMIN_TOKEN=your-secret-admin-token-here
   ```

5. **Run the application**:
   - To start the **public site** (on port 8000):
     ```bash
     python run_public.py
     ```
     Or with uvicorn directly:
     ```bash
     uvicorn run_public:app --reload --host 0.0.0.0 --port 8000
     ```
   - To start the **admin backend** (on port 8001):
     ```bash
     python run_admin.py
     ```

6. **Open your browser**:
   - Public site: `http://localhost:8000`
   - Admin backend: `http://127.0.0.1:8001`

## Usage

### Viewing the Portfolio
- **Home**: `http://localhost:8000/` - View introduction and skills
- **Projects**: `http://localhost:8000/projects` - See all projects
- **Blog**: `http://localhost:8000/blog` - Read blog posts

### Adding Projects (Admin)
To add a new project via the HTMX form on the Projects page:

1. Navigate to `http://localhost:8000/projects`
2. Scroll to the "Add New Project" form
3. Enter your admin token (set in `.env`)
4. Fill in project details
5. Submit the form - the project will be added dynamically!

### Adding Blog Posts
Blog posts are written in Markdown and stored in the `blog_posts/` directory:

1. Create a new `.md` file in `blog_posts/`:
   ```bash
   touch blog_posts/my-new-post.md
   ```

2. Write your post in Markdown format:
   ```markdown
   # My New Blog Post
   
   This is the content of my post...
   ```

3. The post will automatically appear in the blog listing!

## Project Structure

```
portfolio/
├── main.py                 # FastAPI application
├── run_public.py           # Public-facing app runner
├── run_admin.py            # Admin app runner
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/            # Jinja2 templates
│   ├── base.html            # Base layout
│   ├── home.html            # Home page
│   ├── projects.html        # Projects page
│   ├── project_item.html    # Project card component
│   ├── blog.html            # Blog listing
│   ├── blog_post.html       # Individual blog post
│   ├── admin_login.html     # Admin login page
│   ├── admin_dashboard.html # Admin dashboard
│   └── contact.html         # Contact page
├── blog_posts/              # Markdown blog posts
│   └── welcome.md           # Sample blog post
├── data/                    # Data storage
│   ├── projects.json        # Projects (auto-created)
│   └── contacts.json        # Contact form submissions
└── static/                  # Static files
    └── css/                 # Additional CSS (if needed)
```

## Future: SQLite Migration Path

The current implementation uses JSON for project storage, making it easy to get started. However, the architecture is designed for easy migration to SQLite for production use.

### Why SQLite?
- Better performance for queries and data operations
- ACID compliance for data integrity
- Support for relationships and complex queries
- Industry-standard SQL practice

### Migration Plan

**Phase 1: Schema Design**
```sql
-- projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Future: blog_posts table
CREATE TABLE blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Phase 2: Implementation**
1. Add SQLite dependencies (sqlite3 is built into Python)
2. Create database initialization script
3. Update `load_projects()` and `save_projects()` functions to use SQL queries
4. Migrate existing JSON data to SQLite
5. Test thoroughly

**Phase 3: Enhanced Features**
- Add edit/delete functionality for projects
- Implement blog post management via admin interface
- Add tags and categories
- Full-text search capabilities

### Code Changes for SQLite Migration

The main changes will be in `main.py`:

```python
import sqlite3

# Database connection
def get_db():
    conn = sqlite3.connect('data/portfolio.db')
    conn.row_factory = sqlite3.Row
    return conn

# Updated load_projects function
def load_projects():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return projects

# Updated save project (now insert)
def add_project(name, description, url):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (name, description, url) VALUES (?, ?, ?)",
        (name, description, url)
    )
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return project_id
```

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reloading when code changes are detected.

### Testing the Admin Authentication
Use curl or any HTTP client to test the admin-protected endpoint:

```bash
curl -X POST http://localhost:8000/projects \
  -H "Authorization: Bearer your-admin-token" \
  -F "name=Test Project" \
  -F "description=A test project" \
  -F "url=https://github.com/test/project"
```

## Production Deployment

### Environment Variables
Ensure you set a strong admin token in production:
```bash
export ADMIN_TOKEN="your-very-secure-random-token-here"
```

### Running with Gunicorn (Production Server)
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contact

**Tom Gair**
- Email: [tom@gair.dev](mailto:tom@gair.dev)
- Website: [gair.dev](https://gair.dev)

## License

This project is personal portfolio code. Feel free to use it as inspiration for your own portfolio!