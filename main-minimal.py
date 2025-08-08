"""
SkillForge AI - Minimal Main Application for Fast Deployment
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Import only the simplified agent routes
from api.routes import agent_routes

# Load environment variables
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SkillForge AI - Career Intelligence Platform",
    version="1.0.0",
    description="AI-Powered Career Intelligence Platform - Fast Deploy Version"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Try to mount static files (optional if they exist)
try:
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
    templates = Jinja2Templates(directory="frontend/templates")
except Exception as e:
    logger.warning(f"Static files not found: {e}")
    templates = None

# Include only agent routes (simplified)
app.include_router(agent_routes.router, prefix="/api/agents", tags=["agents"])

@app.get("/")
async def root():
    """Root endpoint - Health check"""
    return {
        "message": "🚀 SkillForge AI - Career Intelligence Platform",
        "status": "active",
        "version": "1.0.0 - Fast Deploy",
        "endpoints": {
            "agents": "/api/agents/list",
            "agent_status": "/api/agents/status/{agent_type}",
            "agent_interact": "/api/agents/interact",
            "agent_capabilities": "/api/agents/capabilities/{agent_type}"
        },
        "features": [
            "✅ 3 AI Agents (Analysis, Workflow, Execution)",
            "✅ Career Intelligence & Skill Assessment",
            "✅ Canadian Job Market Data",
            "✅ Salary Benchmarking",
            "✅ Real-time AI Interactions"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
