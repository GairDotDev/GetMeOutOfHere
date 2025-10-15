"""
Job scheduler for background tasks.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime


class JobScheduler:
    """Background job scheduler."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
    
    def add_job(self, func, trigger, job_id: str, **kwargs):
        """Add a job to the scheduler."""
        self.scheduler.add_job(func, trigger, id=job_id, replace_existing=True, **kwargs)
    
    def add_cron_job(self, func, hour: int = 9, minute: int = 0, job_id: str = None):
        """
        Add a cron job that runs daily.
        
        Args:
            func: Function to execute
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
            job_id: Unique job identifier
        """
        trigger = CronTrigger(hour=hour, minute=minute)
        self.add_job(func, trigger, job_id or f"cron_{func.__name__}")
    
    def remove_job(self, job_id: str):
        """Remove a job from scheduler."""
        self.scheduler.remove_job(job_id)
    
    def get_jobs(self):
        """Get all scheduled jobs."""
        return self.scheduler.get_jobs()
    
    def shutdown(self):
        """Shutdown scheduler."""
        self.scheduler.shutdown()


# Global scheduler instance
scheduler = JobScheduler()


def sample_job():
    """Sample background job."""
    print(f"[{datetime.now()}] Sample job executed!")


# Example: Schedule a daily job
# scheduler.add_cron_job(sample_job, hour=9, minute=0, job_id="daily_scrape")
