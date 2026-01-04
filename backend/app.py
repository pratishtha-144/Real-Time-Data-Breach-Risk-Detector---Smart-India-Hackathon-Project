"""
Main FastAPI Application
Entry point for the Data Breach Risk Detector backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.dashboard_routes import router
from database.db import init_db

# Initialize FastAPI app
app = FastAPI(
    title="Data Breach Risk Detector API",
    description="Real-time security risk detection system for hackathon demo",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["Security Scanner"])

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database when server starts"""
    init_db()
    print("\n" + "="*60)
    print("🚀 Data Breach Risk Detector - Backend Started")
    print("="*60)
    print("📡 Server running on: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🎯 Frontend Dashboard: Open frontend/dashboard.html")
    print("="*60 + "\n")

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # Auto-reload on code changes (for development)
    )
