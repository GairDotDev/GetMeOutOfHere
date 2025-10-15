"""
Job service for managing job listings and applications.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlmodel import Session, select
from core.database import JobApplication, JobListing


class JobService:
    """Service for job-related operations."""
    
    def __init__(self, session: Session):
        """Initialize job service."""
        self.session = session
    
    def get_all_jobs(self, limit: int = 100, offset: int = 0) -> List[JobListing]:
        """Get all job listings."""
        statement = select(JobListing).order_by(JobListing.scraped_at.desc()).limit(limit).offset(offset)
        results = self.session.exec(statement)
        return list(results)
    
    def get_job_by_id(self, job_id: int) -> Optional[JobListing]:
        """Get job by ID."""
        return self.session.get(JobListing, job_id)
    
    def get_high_score_jobs(self, threshold: float = 8.5, limit: int = 50) -> List[JobListing]:
        """Get jobs above score threshold."""
        statement = (
            select(JobListing)
            .where(JobListing.score >= threshold)
            .order_by(JobListing.score.desc())
            .limit(limit)
        )
        results = self.session.exec(statement)
        return list(results)
    
    def create_job_listing(self, job_data: Dict[str, Any]) -> JobListing:
        """Create a new job listing."""
        job = JobListing(**job_data)
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job
    
    def get_all_applications(self, limit: int = 100, offset: int = 0) -> List[JobApplication]:
        """Get all job applications."""
        statement = (
            select(JobApplication)
            .order_by(JobApplication.applied_at.desc())
            .limit(limit)
            .offset(offset)
        )
        results = self.session.exec(statement)
        return list(results)
    
    def get_applications_today(self) -> int:
        """Get count of applications submitted today."""
        today = datetime.utcnow().date()
        statement = select(JobApplication).where(
            JobApplication.applied_at >= datetime.combine(today, datetime.min.time())
        )
        results = self.session.exec(statement)
        return len(list(results))
    
    def create_application(self, application_data: Dict[str, Any]) -> JobApplication:
        """Create a new job application record."""
        application = JobApplication(**application_data)
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)
        return application
    
    def has_applied(self, job_url: str) -> bool:
        """Check if already applied to a job."""
        statement = select(JobApplication).where(JobApplication.job_url == job_url)
        result = self.session.exec(statement).first()
        return result is not None
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics."""
        total_jobs = len(self.session.exec(select(JobListing)).all())
        total_applications = len(self.session.exec(select(JobApplication)).all())
        applications_today = self.get_applications_today()
        
        # Get recent high-score jobs
        high_score_jobs = self.get_high_score_jobs(threshold=8.5, limit=5)
        
        return {
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'applications_today': applications_today,
            'high_score_jobs': high_score_jobs
        }
