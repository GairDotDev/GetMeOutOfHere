"""
Auto-application module for submitting job applications.
"""

import json
import os
import time
from typing import Dict, List, Optional
from datetime import datetime


class AutoApplier:
    """Handles automatic job application submission."""
    
    def __init__(self, applied_jobs_file: str = "./applied_jobs.json", 
                 max_applications_per_day: int = 10,
                 delay_between_applications: int = 30,
                 dry_run: bool = False):
        """
        Initialize the auto applier.
        
        Args:
            applied_jobs_file: Path to file tracking applied jobs
            max_applications_per_day: Maximum number of applications per day
            delay_between_applications: Delay in seconds between applications
            dry_run: If True, simulate applications without actually applying
        """
        self.applied_jobs_file = applied_jobs_file
        self.max_applications_per_day = max_applications_per_day
        self.delay_between_applications = delay_between_applications
        self.dry_run = dry_run
        self.applied_jobs = self._load_applied_jobs()
    
    def _load_applied_jobs(self) -> Dict:
        """
        Load the record of previously applied jobs.
        
        Returns:
            Dictionary of applied jobs
        """
        if os.path.exists(self.applied_jobs_file):
            with open(self.applied_jobs_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_applied_jobs(self) -> None:
        """Save the record of applied jobs to file."""
        with open(self.applied_jobs_file, 'w') as f:
            json.dump(self.applied_jobs, f, indent=2)
    
    def has_applied(self, job_url: str) -> bool:
        """
        Check if we've already applied to this job.
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            True if already applied, False otherwise
        """
        return job_url in self.applied_jobs
    
    def get_applications_today(self) -> int:
        """
        Get the number of applications submitted today.
        
        Returns:
            Count of today's applications
        """
        today = datetime.now().strftime('%Y-%m-%d')
        count = 0
        
        for job_data in self.applied_jobs.values():
            if job_data.get('applied_date', '').startswith(today):
                count += 1
        
        return count
    
    def can_apply(self, job_url: str) -> bool:
        """
        Check if we can apply to this job (not already applied, under daily limit).
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            True if we can apply, False otherwise
        """
        if self.has_applied(job_url):
            return False
        
        if self.get_applications_today() >= self.max_applications_per_day:
            return False
        
        return True
    
    def apply(self, job: Dict, resume_path: Optional[str], 
             cover_letter_path: Optional[str], score: float) -> bool:
        """
        Submit an application for a job.
        
        Args:
            job: Dictionary containing job details
            resume_path: Path to the resume file
            cover_letter_path: Path to the cover letter file
            score: The calculated score for this job
            
        Returns:
            True if application was submitted successfully, False otherwise
        """
        job_url = job.get('url', '')
        
        if not self.can_apply(job_url):
            print(f"Cannot apply to {job.get('title')} - already applied or daily limit reached")
            return False
        
        if not resume_path:
            print(f"Cannot apply to {job.get('title')} - no resume available")
            return False
        
        # Simulate or perform actual application
        if self.dry_run:
            print(f"\n[DRY RUN] Would apply to:")
        else:
            print(f"\n[APPLYING] Submitting application to:")
        
        print(f"  Title: {job.get('title')}")
        print(f"  Company: {job.get('company')}")
        print(f"  Location: {job.get('location')}")
        print(f"  Score: {score}/10")
        print(f"  Resume: {resume_path}")
        print(f"  Cover Letter: {cover_letter_path or 'None'}")
        print(f"  URL: {job_url}")
        
        if not self.dry_run:
            # In a real implementation, this would:
            # 1. Navigate to the job posting URL
            # 2. Fill out the application form
            # 3. Upload resume and cover letter
            # 4. Submit the application
            # 
            # This could be done using Selenium WebDriver:
            # - Navigate to job_url
            # - Locate and fill form fields
            # - Upload documents
            # - Click submit button
            
            success = self._submit_application(job, resume_path, cover_letter_path)
            
            if success:
                # Record the application
                self.applied_jobs[job_url] = {
                    'title': job.get('title'),
                    'company': job.get('company'),
                    'location': job.get('location'),
                    'score': score,
                    'applied_date': datetime.now().isoformat(),
                    'resume_used': resume_path,
                    'cover_letter_used': cover_letter_path
                }
                self._save_applied_jobs()
                print("  ✓ Application submitted successfully!")
                
                # Rate limiting
                time.sleep(self.delay_between_applications)
                return True
            else:
                print("  ✗ Application failed")
                return False
        else:
            print("  [DRY RUN] Application not actually submitted")
            return True
    
    def _submit_application(self, job: Dict, resume_path: str, 
                          cover_letter_path: Optional[str]) -> bool:
        """
        Actually submit the application (placeholder for real implementation).
        
        In production, this would use Selenium or API calls to submit the application.
        
        Args:
            job: Job details
            resume_path: Path to resume
            cover_letter_path: Path to cover letter
            
        Returns:
            True if successful, False otherwise
        """
        # Placeholder for actual application submission logic
        # In reality, this would use Selenium WebDriver or API calls
        
        # For now, just simulate success
        print("  [Note: Actual application submission not implemented - requires Selenium]")
        return True
    
    def get_application_summary(self) -> Dict:
        """
        Get summary of applications.
        
        Returns:
            Dictionary with application statistics
        """
        total_applications = len(self.applied_jobs)
        today_applications = self.get_applications_today()
        
        return {
            'total_applications': total_applications,
            'applications_today': today_applications,
            'daily_limit': self.max_applications_per_day,
            'remaining_today': max(0, self.max_applications_per_day - today_applications)
        }
