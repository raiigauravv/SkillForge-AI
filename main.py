"""
SkillForge AI - Main Application Entry Point
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

# Import API routes
from api.routes import workflow_routes, agent_routes, crew_routes
from api.routes.analytics_routes import router as analytics_router
from api.routes.career_intelligence_routes import router as career_intelligence_router
from src.config.settings import Settings
from src.utils.logger import setup_logging
from database.mongodb_config import db_manager

# Load environment variables
load_dotenv()

# Initialize settings
settings = Settings()

# Setup logging
setup_logging(settings.LOG_LEVEL, settings.LOG_FILE)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Career Intelligence Platform - SkillForge AI"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Include API routes
app.include_router(workflow_routes.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(agent_routes.router, prefix="/api/agents", tags=["agents"])
app.include_router(crew_routes.router, prefix="/api/crews", tags=["crews"])
app.include_router(analytics_router, prefix="/api", tags=["analytics"])
app.include_router(career_intelligence_router, prefix="/api", tags=["career-intelligence"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
async def api_root():
    """Root API endpoint - returns basic info about the application"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "framework": "CrewAI",
        "description": "AI-Powered Career Intelligence Platform",
        "endpoints": {
            "workflows": "/api/workflows",
            "agents": "/api/agents", 
            "crews": "/api/crews"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "framework": "CrewAI",
        "version": settings.APP_VERSION
    }

@app.get("/api/info")
async def system_info():
    """System information endpoint"""
    return {
        "system": "SkillForge AI",
        "framework": "CrewAI v0.152.0",
        "backend": "FastAPI + Python",
        "agents": ["WorkflowAgent", "AnalysisAgent", "ExecutionAgent"],
        "crews": ["WorkflowCrew"],
        "features": [
            "Multi-agent workflow automation",
            "Real-time agent coordination", 
            "Custom tool integration",
            "Web-based interface",
            "API-driven architecture"
        ]
    }

if __name__ == "__main__":
    import os
    
    # Railway deployment configuration
    port = int(os.environ.get("PORT", settings.PORT))
    host = "0.0.0.0"  # Railway requires 0.0.0.0
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Running on {host}:{port}")
    logger.info("Framework: CrewAI - Multi-Agent Workflow Automation")
    logger.info("Environment: Production deployment ready")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level=settings.LOG_LEVEL.lower()
    )
