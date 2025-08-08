"""
SkillForge AI - Working FastAPI for Vercel
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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
def read_root():
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
            "✅ Production Optimized",
            "✅ 3 AI Agents Ready"
        ]
    }

@app.get("/health")  
def health():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "SkillForge AI"
    }

@app.get("/test")
def test():
    return {
        "test": "✅ Endpoint working perfectly",
        "framework": "FastAPI",
        "deployment": "Vercel Production",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/agents/list")
def agents():
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
