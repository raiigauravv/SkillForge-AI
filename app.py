"""
Simple test entry point for debugging
"""

from fastapi import FastAPI

# Create a minimal working app
app = FastAPI(title="SkillForge AI Test")

@app.get("/")
async def root():
    return {"message": "SkillForge AI is working!", "status": "success"}

@app.get("/test")
async def test():
    return {"test": "endpoint working", "framework": "FastAPI"}

# Export for Vercel
handler = app
