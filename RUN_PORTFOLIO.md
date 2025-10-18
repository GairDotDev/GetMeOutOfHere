# 🚀 Run Your Portfolio

## Quick Start

### 1. Navigate to your project
```powershell
cd C:\Users\Tom\Documents\Projects\portfolio
```

### 2. Activate virtual environment (if using venv)
```powershell
.\venv\Scripts\activate
```

### 3. Run the development server
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Open in browser
```
http://127.0.0.1:8000
```

---

## What to Check

✅ **Home Page** (`/`)
- New hero: "I build reliable software and simple systems"
- "Open to Employment, Freelance, and Collaboration" badge
- About Me section with bio
- 7 skill cards (Python, FastAPI, SQLite, HTMX/Jinja, Docker, GitHub, AI-assisted Dev)

✅ **Projects Page** (`/projects`)
- 3 new projects: Runelight, Normal Is An Illusion, JobScraper
- Enhanced card design with hover effects
- Responsive grid layout
- Tag filtering with HTMX

✅ **Contact Page** (`/contact`)
- "Get In Touch" header
- "Open to employment..." messaging
- Enhanced form styling
- Direct contact buttons (email + GitHub)

✅ **Footer** (all pages)
- "© 2025 Tom Gair"
- "Built with FastAPI, Jinja2, and AI-assisted design"

---

## Troubleshooting

### Port already in use?
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

### Virtual environment issues?
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Want to stop the server?
Press `Ctrl + C` in the terminal

---

## Admin Dashboard

Visit: `http://127.0.0.1:8000/admin-login`

Default credentials (set in `.env` or environment):
- Username: `admin`
- Password: `change-me-in-production`

**⚠️ Remember to change these before deploying to production!**

---

## Next Steps

1. ✅ Review the site in your browser
2. ✅ Test dark mode toggle (top right)
3. ✅ Try the contact form
4. ✅ Check responsive design (resize browser)
5. ✅ Review project cards
6. Create `.env` file with your admin credentials
7. Add more blog posts to `/content/blog/` if desired
8. Deploy to production when ready

---

## Files to Review

- `UPGRADE_SUMMARY.md` - Complete list of changes
- `CHANGES_DIFF.md` - Visual diff of all modifications
- `DEPLOYMENT_NOTES.md` - Production deployment guide

---

**Status: ✅ Ready for local preview!**


