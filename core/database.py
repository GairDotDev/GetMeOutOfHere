"""
Database models and connection management.
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session
from core.config import settings


class JobApplication(SQLModel, table=True):
    """Job application record."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    job_title: str
    company: str
    job_url: str = Field(unique=True, index=True)
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    score: float
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="applied")  # applied, rejected, interview, offer
    resume_used: Optional[str] = None
    cover_letter_used: Optional[str] = None


class JobListing(SQLModel, table=True):
    """Job listing from scraping."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    job_title: str
    company: str
    job_url: str = Field(unique=True, index=True)
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    score: Optional[float] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    job_board: str


# Create engine
engine = create_engine(settings.database_url, echo=False)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
