# Portfolio Deployment Notes

## Local Development

To run the portfolio locally:

```bash
# Activate virtual environment (if using)
# Windows:
venv\Scripts\activate

# Run the application
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Then visit: `http://127.0.0.1:8000`

## Production Deployment

### Requirements
- Python 3.9+
- All packages in `requirements.txt`
- Environment variables (`.env` file):
  ```
  ADMIN_USERNAME=your_admin_username
  ADMIN_PASSWORD=your_secure_password
  ADMIN_TOKEN=your_secure_token
  ```

### Run Command
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment (recommended)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Recent Updates

### Home Page
- Updated hero section with new tagline: "I build reliable software and simple systems"
- Added "Open to Employment, Freelance, and Collaboration" badge
- Replaced tech stack section with About Me section
- Added simplified skill cards for: Python, FastAPI, SQLite, HTMX/Jinja, Docker, GitHub, AI-assisted Dev

### Projects Page
- Updated with three featured projects:
  - Runelight (local-first camera stack)
  - Normal Is An Illusion (emotional journaling platform)
  - JobScraper (job automation and data cleaner)
- Enhanced project card design with better hover effects
- Improved responsive grid layout

### Contact Page
- Added page header with clear messaging
- Enhanced form styling
- Improved direct contact buttons

### Footer
- Updated with: "© 2025 Tom Gair"
- Added: "Built with FastAPI, Jinja2, and AI-assisted design"

### General Cleanup
- Removed unused imports (hashlib, timedelta, Response)
- Added docstring header to main.py
- Cleaned up code comments

## Features

- FastAPI backend with Jinja2 templates
- HTMX for dynamic interactions
- Tailwind CSS for styling
- Dark mode support
- Admin dashboard with authentication
- Blog system with Markdown support
- Contact form with data persistence
- Project showcase with filtering
- SEO-friendly (robots.txt, sitemap.xml)


