"""
Main application entry point for GetMeOutOfHere job scraper.
"""

import sys
import os
from typing import List, Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_loader import ConfigLoader
from job_scraper import JobScraper
from job_scorer import JobScorer
from document_selector import DocumentSelector
from auto_applier import AutoApplier


class JobApplicationBot:
    """Main application class that coordinates all components."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the job application bot.
        
        Args:
            config_path: Path to configuration file
        """
        print("Initializing GetMeOutOfHere Job Application Bot...")
        
        # Load configuration
        try:
            self.config = ConfigLoader(config_path)
            print("✓ Configuration loaded successfully")
        except Exception as e:
            print(f"✗ Error loading configuration: {e}")
            sys.exit(1)
        
        # Initialize components
        self.scraper = JobScraper(
            delay=self.config.get('rate_limiting.delay_between_scrapes', 5)
        )
        
        self.scorer = JobScorer(
            weights=self.config.get_scoring_weights(),
            preferences=self.config.get_preferences()
        )
        
        self.document_selector = DocumentSelector(
            documents_config=self.config.get_documents_config()
        )
        
        app_config = self.config.get('application', {})
        self.applier = AutoApplier(
            applied_jobs_file=app_config.get('applied_jobs_file', './applied_jobs.json'),
            max_applications_per_day=app_config.get('max_applications_per_day', 10),
            delay_between_applications=self.config.get('rate_limiting.delay_between_applications', 30),
            dry_run=app_config.get('dry_run', False)
        )
        
        self.score_threshold = self.config.get_score_threshold()
        self.auto_apply = app_config.get('auto_apply', True)
        
        print("✓ All components initialized")
    
    def run(self) -> None:
        """Run the job application bot."""
        print("\n" + "="*60)
        print("Starting job search and application process...")
        print("="*60)
        
        # Validate documents
        print("\nValidating documents...")
        if not self.document_selector.validate_documents():
            print("Warning: Some documents are missing. Applications may fail.")
        
        # Get application summary
        summary = self.applier.get_application_summary()
        print(f"\nApplication Summary:")
        print(f"  Total applications: {summary['total_applications']}")
        print(f"  Applications today: {summary['applications_today']}/{summary['daily_limit']}")
        print(f"  Remaining today: {summary['remaining_today']}")
        
        if summary['remaining_today'] == 0:
            print("\n✗ Daily application limit reached. Exiting.")
            return
        
        # Get search parameters
        search_config = self.config.get('job_search', {})
        keywords = search_config.get('keywords', [])
        locations = search_config.get('locations', [])
        job_boards = search_config.get('job_boards', [])
        
        print(f"\nSearch Parameters:")
        print(f"  Keywords: {', '.join(keywords)}")
        print(f"  Locations: {', '.join(locations)}")
        print(f"  Job Boards: {', '.join(job_boards)}")
        print(f"  Score Threshold: {self.score_threshold}/10")
        print(f"  Auto-apply: {'Enabled' if self.auto_apply else 'Disabled'}")
        
        # Scrape jobs
        print("\n" + "-"*60)
        print("Scraping job postings...")
        print("-"*60)
        jobs = self.scraper.scrape_jobs(keywords, locations, job_boards)
        print(f"\n✓ Found {len(jobs)} job postings")
        
        # Score and filter jobs
        print("\n" + "-"*60)
        print("Scoring job postings...")
        print("-"*60)
        
        scored_jobs = []
        for job in jobs:
            score = self.scorer.score_job(job)
            scored_jobs.append({
                'job': job,
                'score': score
            })
        
        # Sort by score (highest first)
        scored_jobs.sort(key=lambda x: x['score'], reverse=True)
        
        # Display results
        print(f"\n{'='*60}")
        print("Job Scoring Results")
        print(f"{'='*60}")
        
        high_score_jobs = [sj for sj in scored_jobs if sj['score'] > self.score_threshold]
        
        print(f"\nJobs above threshold ({self.score_threshold}/10): {len(high_score_jobs)}")
        print(f"Jobs below threshold: {len(scored_jobs) - len(high_score_jobs)}")
        
        # Process high-scoring jobs
        if high_score_jobs:
            print(f"\n{'='*60}")
            print("High-Scoring Jobs (above threshold)")
            print(f"{'='*60}")
            
            applications_submitted = 0
            
            for idx, scored_job in enumerate(high_score_jobs, 1):
                job = scored_job['job']
                score = scored_job['score']
                
                print(f"\n[{idx}] {job.get('title')} at {job.get('company')}")
                print(f"    Score: {score}/10 ⭐")
                print(f"    Location: {job.get('location')}")
                print(f"    Salary: ${job.get('salary_min', 0):,} - ${job.get('salary_max', 0):,}")
                print(f"    URL: {job.get('url')}")
                
                # Check if we can apply
                if not self.applier.can_apply(job.get('url', '')):
                    print(f"    Status: ⊘ Already applied or daily limit reached")
                    continue
                
                # Select documents
                resume_path, cover_letter_path = self.document_selector.select_documents(job)
                
                # Apply if auto-apply is enabled
                if self.auto_apply:
                    success = self.applier.apply(job, resume_path, cover_letter_path, score)
                    if success:
                        applications_submitted += 1
                else:
                    print(f"    Status: ℹ Auto-apply disabled (manual review required)")
                
                # Check if we've reached daily limit
                if applications_submitted >= self.applier.max_applications_per_day:
                    print("\n✓ Daily application limit reached.")
                    break
        
        # Display all jobs (summary)
        print(f"\n{'='*60}")
        print("All Jobs Summary")
        print(f"{'='*60}")
        
        for idx, scored_job in enumerate(scored_jobs, 1):
            job = scored_job['job']
            score = scored_job['score']
            
            status = "⭐" if score > self.score_threshold else "  "
            print(f"{status} [{score:4.1f}/10] {job.get('title')[:40]:40} | {job.get('company')[:20]:20}")
        
        # Final summary
        print(f"\n{'='*60}")
        print("Session Complete")
        print(f"{'='*60}")
        
        final_summary = self.applier.get_application_summary()
        print(f"Total jobs scraped: {len(jobs)}")
        print(f"High-scoring jobs: {len(high_score_jobs)}")
        print(f"Applications today: {final_summary['applications_today']}/{final_summary['daily_limit']}")
        print(f"Total applications all-time: {final_summary['total_applications']}")


def main():
    """Main entry point."""
    # Check for config file
    config_path = "config.yaml"
    
    try:
        bot = JobApplicationBot(config_path)
        bot.run()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
