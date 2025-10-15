"""
Run the public portfolio site on port 8000.
This script starts the FastAPI application for the public-facing portfolio.
"""
import uvicorn
from main import app

if __name__ == "__main__":
    # Run public site on all interfaces, port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
