"""
FastAPI application setup.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from core.config import settings
from core.database import create_db_and_tables
from web.routes import dashboard, jobs, settings as settings_routes


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version
    )
    
    # Create database tables
    create_db_and_tables()
    
    # Mount static files
    static_path = Path(__file__).parent / "static"
    static_path.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    # Include routers
    app.include_router(dashboard.router, prefix="", tags=["Dashboard"])
    app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
    app.include_router(settings_routes.router, prefix="/settings", tags=["Settings"])
    
    @app.on_event("startup")
    async def startup_event():
        """Run on application startup."""
        print(f"Starting {settings.app_title} v{settings.app_version}")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Run on application shutdown."""
        print("Shutting down application...")
    
    return app


app = create_app()
