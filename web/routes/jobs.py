"""
Jobs routes.
"""

from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from pathlib import Path
from typing import Optional

from core.database import get_session
from services.job_service import JobService

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def list_jobs(
    request: Request,
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List all jobs."""
    job_service = JobService(session)
    jobs = job_service.get_all_jobs(limit=limit, offset=offset)
    
    return templates.TemplateResponse(
        "jobs.html",
        {
            "request": request,
            "jobs": jobs,
            "page_title": "Job Listings"
        }
    )


@router.get("/applications", response_class=HTMLResponse)
async def list_applications(
    request: Request,
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List all applications."""
    job_service = JobService(session)
    applications = job_service.get_all_applications(limit=limit, offset=offset)
    
    return templates.TemplateResponse(
        "applications.html",
        {
            "request": request,
            "applications": applications,
            "page_title": "My Applications"
        }
    )


@router.get("/{job_id}", response_class=HTMLResponse)
async def view_job(
    request: Request,
    job_id: int,
    session: Session = Depends(get_session)
):
    """View single job details."""
    job_service = JobService(session)
    job = job_service.get_job_by_id(job_id)
    
    return templates.TemplateResponse(
        "job_detail.html",
        {
            "request": request,
            "job": job,
            "page_title": f"Job: {job.job_title if job else 'Not Found'}"
        }
    )
