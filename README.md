# GetMeOutOfHere

An automated Python-based job searching tool that scrapes job postings, scores them using a weighted algorithm, and automatically applies if the score exceeds 8.5/10.

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

3. Set up your configuration:
```bash
cp config.example.yaml config.yaml
```

4. Edit `config.yaml` with your preferences, scoring weights, and search parameters.

5. Create directories for your documents:
```bash
mkdir -p resumes cover_letters
```

6. Add your resumes and cover letters to the respective directories.

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

Run the job application bot:

```bash
cd src
python main.py
```

### Dry Run Mode

To test without actually applying:

1. Set `dry_run: true` in `config.yaml`
2. Run the bot to see what jobs would be applied to

### Output

The bot will:
1. Scrape job postings from configured job boards
2. Score each job based on your preferences
3. Display all jobs with their scores
4. Automatically apply to jobs scoring above threshold
5. Track applications in `applied_jobs.json`

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
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── config_loader.py     # Configuration management
│   ├── job_scraper.py       # Job scraping logic
│   ├── job_scorer.py        # Job scoring algorithm
│   ├── document_selector.py # Resume/cover letter selection
│   └── auto_applier.py      # Auto-application logic
├── resumes/                 # Your resume files
├── cover_letters/           # Your cover letter files
├── config.yaml              # Your configuration (create from example)
├── config.example.yaml      # Example configuration
├── requirements.txt         # Python dependencies
├── applied_jobs.json        # Tracking file (auto-generated)
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
