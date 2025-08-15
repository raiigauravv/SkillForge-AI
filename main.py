#!/usr/bin/env python3
"""
SkillForge AI - FORCE REDEPLOY VERSION
Production-ready FastAPI application optimized for free hosting
DEPLOYMENT TIMESTAMP: 2025-01-15-16:30-FORCE-REBUILD
"""

import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print("🚀 SkillForge AI starting up...")
    print("🌟 Simplified deployment - No MongoDB required")
    yield
    print("🛑 SkillForge AI shutting down...")


# Initialize FastAPI with lifespan
app = FastAPI(
    title="SkillForge AI",
    description="AI-Powered Career Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates and Static Files
templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Main page route - serve HTML dashboard at root
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# DEBUGGING: Simple HTML test route
@app.get("/test")
async def test_html():
    return {"test": "If you see this JSON, templates are broken. If you see HTML, templates work."}

@app.get("/testhtml")  
async def test_html_route(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API health check endpoint
@app.get("/api")
async def api_root():
    return {
        "message": "🚀 SkillForge AI - Career Intelligence Platform",
        "status": "running",
        "version": "1.0.0", 
        "deployment": "simplified",
        "timestamp": "2025-01-15-FIXED"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "not_required"}

# Additional page routes
@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/analytics")
async def analytics_dashboard(request: Request):
    return templates.TemplateResponse("index_analytics.html", {"request": request})

# Import route modules (simplified versions)
try:
    from api.routes import career_intelligence_routes, analytics_routes
    
    # Include routers
    app.include_router(career_intelligence_routes.router, prefix="/api/career", tags=["Career Intelligence"])
    app.include_router(analytics_routes.router, prefix="/api/analytics", tags=["Analytics"])
    
    print("✅ All routes loaded successfully")
except ImportError as e:
    print(f"⚠️ Some routes not available: {e}")

if __name__ == "__main__":
    # Production configuration
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"🌐 Starting server on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=False)
