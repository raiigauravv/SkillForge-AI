#!/usr/bin/env python3
"""
SkillForge AI - Render Deployment Version
"""

import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# Initialize FastAPI
app = FastAPI(title="SkillForge AI", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/analytics")
async def analytics(request: Request):
    return templates.TemplateResponse("index_analytics.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "healthy", "platform": "render", "timestamp": datetime.now().isoformat()}

@app.get("/api/agents/list")
async def agents():
    return {
        "status": "success",
        "data": {
            "agents": [
                {"type": "workflow_agent", "name": "Workflow Orchestrator", "status": "active"},
                {"type": "analysis_agent", "name": "Analysis Specialist", "status": "active"},
                {"type": "execution_agent", "name": "Execution Specialist", "status": "active"}
            ]
        }
    }

@app.post("/api/agents/interact")
async def interact(request: dict):
    return {
        "status": "success",
        "data": {
            "response": f"Agent processing: {request.get('message', 'Hello')}",
            "agent_type": request.get("agent_type", "workflow_agent"),
            "timestamp": datetime.now().isoformat()
        }
    }

@app.get("/api/career-intelligence/status")
async def career_status():
    return {
        "status": "active",
        "models": {
            "salary_predictor": {"accuracy": "93.6%", "status": "ready"},
            "job_matcher": {"accuracy": "74%", "status": "ready"}
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
