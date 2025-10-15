"""
Settings routes.
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import yaml

from core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings page."""
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "settings": settings.config,
            "page_title": "Settings"
        }
    )


@router.post("/update")
async def update_settings(
    score_threshold: float = Form(...),
    auto_apply: bool = Form(False),
    dry_run: bool = Form(True),
    max_applications_per_day: int = Form(10)
):
    """Update settings."""
    # Update configuration
    settings.config['score_threshold'] = score_threshold
    settings.config['application']['auto_apply'] = auto_apply
    settings.config['application']['dry_run'] = dry_run
    settings.config['application']['max_applications_per_day'] = max_applications_per_day
    
    # Save to file
    with open(settings.config_path, 'w') as f:
        yaml.dump(settings.config, f, default_flow_style=False)
    
    return RedirectResponse(url="/settings", status_code=303)
