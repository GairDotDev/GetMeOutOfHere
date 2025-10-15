"""
Run the admin backend on 127.0.0.1:8001.
This script starts the FastAPI application for the admin interface.
The admin should be accessed via reverse proxy with Basic Auth.
"""
import uvicorn
from main import app

if __name__ == "__main__":
    # Run admin backend on localhost only, port 8001
    # This should be proxied by Nginx with Basic Auth + optional IP allowlist
    uvicorn.run(app, host="127.0.0.1", port=8001)
