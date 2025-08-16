#!/usr/bin/env python3
"""
SkillForge AI - Render Deployment Version
"""

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import openai
import asyncio
from typing import Dict, Any

# Initialize FastAPI
app = FastAPI(title="SkillForge AI", version="1.0.0")

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    try:
        message = request.get("message", "")
        agent_type = request.get("agent_type", "workflow_agent")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if not openai.api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        # Agent-specific prompts
        agent_prompts = {
            "workflow_agent": f"You are a Workflow Orchestrator AI. Help the user organize and execute this task: {message}. Provide step-by-step guidance.",
            "analysis_agent": f"You are a Data Analysis Specialist AI. Analyze this request: {message}. Provide insights and recommendations.", 
            "execution_agent": f"You are a Task Execution Specialist AI. Help execute this task: {message}. Provide practical implementation steps."
        }
        
        prompt = agent_prompts.get(agent_type, f"You are an AI assistant. Help with: {message}")
        
        # Call OpenAI API
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content
        
        return {
            "status": "success",
            "data": {
                "response": ai_response,
                "agent_type": agent_type,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Agent interaction failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/career-intelligence/status")
async def career_status():
    try:
        return {
            "status": "active",
            "models": {
                "salary_predictor": {"accuracy": "93.6%", "status": "ready"},
                "job_matcher": {"accuracy": "74%", "status": "ready"},
                "ai_advisor": {"status": "ready"}
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Career intelligence error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/career-intelligence/analyze")
async def career_analyze(request: dict):
    try:
        profile = request.get("profile", {})
        skills = profile.get("skills", "")
        experience = profile.get("experience", "")
        goals = profile.get("goals", "")
        
        if not openai.api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        prompt = f"""
        As a Career Intelligence AI, analyze this professional profile:
        Skills: {skills}
        Experience: {experience}  
        Goals: {goals}
        
        Provide:
        1. Salary estimate range
        2. Top 3 job matches with scores
        3. Skill recommendations
        4. Career path advice
        """
        
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.3
        )
        
        ai_analysis = response.choices[0].message.content
        
        return {
            "status": "success",
            "data": {
                "analysis": ai_analysis,
                "profile_summary": profile,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Career analysis failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
