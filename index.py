"""
Vercel Python Handler - Index Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="SkillForge AI - Career Intelligence Platform",
    version="1.0.0",
    description="AI-Powered Career Intelligence Platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - Health check with feature overview"""
    return {
        "message": "🚀 SkillForge AI - Career Intelligence Platform",
        "status": "active",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "test": "/test",
            "agents_list": "/api/agents/list"
        },
        "features": [
            "✅ FastAPI Backend",
            "✅ CORS Enabled", 
            "✅ Health Checks",
            "✅ Serverless Ready",
            "✅ Production Optimized"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "SkillForge AI"
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify app is working"""
    return {
        "test": "✅ Endpoint working perfectly",
        "framework": "FastAPI",
        "deployment": "Vercel Production",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/agents/list")
async def list_agents():
    """Simple agents list without external dependencies"""
    return {
        "agents": [
            {
                "type": "analysis_agent",
                "name": "Career Analysis Agent",
                "status": "active",
                "features": ["Market Intelligence", "Salary Analysis", "Skill Assessment"]
            },
            {
                "type": "workflow_agent", 
                "name": "Workflow Optimization Agent",
                "status": "active",
                "features": ["Process Design", "Task Automation", "Timeline Planning"]
            },
            {
                "type": "execution_agent",
                "name": "Task Execution Agent", 
                "status": "active",
                "features": ["Implementation", "Monitoring", "Quality Assurance"]
            }
        ],
        "total": 3,
        "framework": "FastAPI",
        "status": "production_ready"
    }

# This is the standard Vercel pattern
handler = app
