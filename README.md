# Get Me Out Of Here

An automated job application system with a web interface built with FastAPI. Scrapes job postings, scores them using a weighted algorithm, and manages applications through an intuitive dashboard.

## Features

- 🔍 **Job Scraping**: Scrapes job postings from multiple job boards (Indeed, LinkedIn)
- 📊 **Weighted Scoring System**: Evaluates jobs on a 0-10 scale based on:
  - Keyword/skill matching (25%)
  - Salary alignment (20%)
  - Location preferences (15%)
  - Company rating (15%)
  - Role seniority match (15%)
  - Benefits and perks (10%)
- 🤖 **Auto-Apply**: Automatically submits applications when score > 8.5/10
- 📄 **Smart Document Selection**: Automatically selects the appropriate resume and cover letter based on job characteristics
- 📈 **Daily Limits**: Respects configurable daily application limits
- 🔄 **Duplicate Prevention**: Tracks applied jobs to avoid duplicate applications
- 🌐 **Rate Limiting**: Built-in delays to respect job board rate limits

## Installation

1. Clone the repository:
```bash
git clone https://github.com/GairDotDev/GetMeOutOfHere.git
cd GetMeOutOfHere
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up your configuration:
```bash
cp config.example.yaml config.yaml
```

4. Edit `config.yaml` with your preferences, or use the web interface to configure settings.

5. Add your resumes to the `resumes/` directory.

## Configuration

Edit `config.yaml` to customize:

- **Score Threshold**: Set the minimum score (0-10) for auto-apply (default: 8.5)
- **Search Parameters**: Keywords, locations, and job boards to search
- **Scoring Weights**: Adjust weights for different scoring criteria (must sum to 1.0)
- **Preferences**: Your salary expectations, required skills, experience level
- **Document Mapping**: Map specific resumes/cover letters to job types
- **Application Settings**: Daily limits, dry run mode, rate limiting

### Example Configuration

```yaml
score_threshold: 8.5

job_search:
  keywords:
    - "software engineer"
    - "python developer"
  locations:
    - "Remote"
    - "San Francisco, CA"

preferences:
  min_salary: 80000
  target_salary: 120000
  required_skills:
    - "Python"
    - "Django"
    - "REST API"
  experience_level: "mid"

application:
  auto_apply: true
  dry_run: false
  max_applications_per_day: 10
```

## Usage

### Web Interface (Recommended)

Run the FastAPI web application:

```bash
python main.py
```

Then open your browser to `http://localhost:8000`

The web interface provides:
- **Dashboard**: Overview of jobs and applications with statistics
- **Jobs**: Browse all scraped job listings with scores
- **Applications**: Track your submitted applications
- **Settings**: Configure preferences, thresholds, and application settings

### Features

- 📊 **Dashboard** with real-time statistics
- 🔍 **Job Listings** with scoring and filtering
- 📝 **Application Tracking** with status updates
- ⚙️ **Settings Management** through web UI
- 🗄️ **SQLite Database** for persistent storage
- ⏰ **Background Jobs** with APScheduler for automated scraping
- 🎨 **Responsive Design** with Jinja2 templates

## Document Selection

The bot automatically selects the best resume and cover letter for each job:

### Resume Selection
- **Backend roles**: Uses `resume_backend.pdf`
- **Frontend roles**: Uses `resume_frontend.pdf`
- **Full-stack roles**: Uses `resume_fullstack.pdf`
- **Data Science roles**: Uses `resume_datascience.pdf`
- **Default**: Uses `resume_general.pdf`

### Cover Letter Selection
- **Startup companies**: Uses `cover_letter_startup.pdf`
- **Enterprise companies**: Uses `cover_letter_enterprise.pdf`
- **Default**: Uses `cover_letter_generic.pdf`

## Scoring System

Jobs are scored on a 0-10 scale using weighted criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Keyword Match | 25% | Matches required and nice-to-have skills |
| Salary Match | 20% | Alignment with salary expectations |
| Location | 15% | Matches preferred locations |
| Company Rating | 15% | Company reputation and ratings |
| Role Seniority | 15% | Match with experience level |
| Benefits | 10% | Quality and quantity of benefits |

### Auto-Apply Threshold

Jobs scoring above **8.5/10** will be automatically applied to (configurable).

## File Structure

```
GetMeOutOfHere/
├── core/                    # Core application modules
│   ├── config.py            # Configuration management
│   └── database.py          # SQLModel database models
├── services/                # Business logic services
│   ├── job_service.py       # Job management service
│   └── scraper_service.py   # Job scraping service
├── jobs/                    # Background job scheduling
│   ├── scheduler.py         # APScheduler setup
│   └── tasks.py             # Background task definitions
├── web/                     # Web interface
│   ├── app.py               # FastAPI application
│   ├── routes/              # API routes
│   │   ├── dashboard.py     # Dashboard routes
│   │   ├── jobs.py          # Job routes
│   │   └── settings.py      # Settings routes
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── jobs.html
│   │   ├── applications.html
│   │   ├── job_detail.html
│   │   └── settings.html
│   └── static/              # CSS, JS, images
│       └── style.css
├── resumes/                 # Your resume files
├── src/                     # Legacy CLI code (deprecated)
├── main.py                  # Application entry point
├── config.yaml              # Your configuration (optional)
├── config.example.yaml      # Example configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## Safety Features

- **Dry Run Mode**: Test without actually applying
- **Daily Limits**: Prevents over-applying
- **Duplicate Prevention**: Tracks applied jobs
- **Rate Limiting**: Respects job board limits
- **Document Validation**: Checks for required files before applying

## Limitations & Disclaimer

⚠️ **Important Notes**:

1. This is a demonstration/framework. Full job board integration requires:
   - API keys or authentication
   - Selenium for dynamic content
   - Compliance with job board terms of service

2. Always review applications before submission in production use

3. Respect job board rate limits and terms of service

4. The actual application submission (`_submit_application`) is a placeholder and needs to be implemented with proper web automation (Selenium) for production use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and personal use.
