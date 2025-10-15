"""
Dashboard routes.
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from pathlib import Path

from core.database import get_session
from services.job_service import JobService

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, session: Session = Depends(get_session)):
    """Dashboard page."""
    job_service = JobService(session)
    stats = job_service.get_dashboard_stats()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "stats": stats,
            "page_title": "Dashboard"
        }
    )
