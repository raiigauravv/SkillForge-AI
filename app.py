"""
SkillForge AI - Working Production App
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Try to include agent routes, with fallback if import fails
try:
    from api.routes.agent_routes import router as agent_router
    app.include_router(agent_router, prefix="/api/agents", tags=["agents"])
    logger.info("✅ Agent routes loaded successfully")
except Exception as e:
    logger.warning(f"⚠️ Could not load agent routes: {e}")

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
            "agents_list": "/api/agents/list",
            "agent_status": "/api/agents/status/{agent_type}",
            "agent_interact": "/api/agents/interact",
            "agent_capabilities": "/api/agents/capabilities/{agent_type}"
        },
        "features": [
            "✅ 3 AI Agents (Analysis, Workflow, Execution)",
            "✅ Career Intelligence & Skill Assessment", 
            "✅ Canadian Job Market Data",
            "✅ Salary Benchmarking",
            "✅ Real-time AI Interactions",
            "✅ Python/SQL/ML Skill Analysis"
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

# Export for Vercel
handler = app
