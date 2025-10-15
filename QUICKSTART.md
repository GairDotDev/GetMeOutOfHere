# Quick Start Guide

## Getting Started with GetMeOutOfHere v2.0

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/GairDotDev/GetMeOutOfHere.git
cd GetMeOutOfHere

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Open your browser to: **http://localhost:8000**

### 3. First Steps

1. **Visit Settings** (http://localhost:8000/settings)
   - Configure your score threshold (default: 8.5)
   - Set max applications per day
   - Enable/disable auto-apply
   - Toggle dry run mode for testing

2. **Add Your Resumes**
   - Place your resume files (PDF, DOCX) in the `resumes/` directory

3. **Configure Job Search** (optional)
   - Edit `config.yaml` or create one from `config.example.yaml`
   - Set keywords, locations, and job boards to scrape

4. **Start Scraping**
   - Use the background scheduler or run scraping tasks manually
   - View scraped jobs on the Jobs page
   - Track applications on the Applications page

### 4. Using the Dashboard

The dashboard provides an overview of:
- Total jobs scraped
- Total applications submitted
- Applications submitted today
- High-scoring jobs (above threshold)

### 5. API Endpoints

The FastAPI application provides several endpoints:

- `GET /` - Dashboard
- `GET /jobs` - List all jobs
- `GET /jobs/{job_id}` - View job details
- `GET /jobs/applications` - List applications
- `GET /settings` - Settings page
- `POST /settings/update` - Update settings

### 6. Database

The application uses SQLite (stored as `getmeoutofhere.db`) with two main tables:
- `joblisting` - Scraped job postings
- `jobapplication` - Application records

### 7. Background Jobs

Configure background jobs in `jobs/scheduler.py` to:
- Automatically scrape jobs on a schedule
- Process applications for high-scoring jobs
- Clean up old data

### 8. Development

Run with auto-reload for development:
```bash
uvicorn web.app:app --reload --host 0.0.0.0 --port 8000
```

### 9. Troubleshooting

**Port already in use:**
```bash
# Change port in main.py or run with:
python -c "import uvicorn; from web.app import app; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

**Database issues:**
```bash
# Delete and recreate database
rm getmeoutofhere.db
python main.py
```

### 10. Next Steps

- Integrate with real job board APIs (Indeed, LinkedIn)
- Add authentication for multi-user support
- Implement email notifications
- Add more sophisticated scoring algorithms
- Deploy to production (Heroku, Railway, etc.)

## Need Help?

Check out the [README.md](README.md) for more detailed information.
