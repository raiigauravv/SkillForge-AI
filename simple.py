"""
Minimal FastAPI for Vercel - Standard Pattern
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from SkillForge AI!", "status": "working"}

@app.get("/health")  
def health():
    return {"status": "healthy"}

@app.get("/api/agents/list")
def agents():
    return {
        "agents": ["analysis_agent", "workflow_agent", "execution_agent"],
        "status": "active"
    }
