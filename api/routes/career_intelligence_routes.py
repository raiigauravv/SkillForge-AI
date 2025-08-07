"""
🎯 CAREER INTELLIGENCE API ROUTES
Advanced API endpoints for Level 1 & Level 2 Career Analytics Integration
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import asyncio

from src.analytics.career_intelligence_engine import career_engine, CareerMetrics

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/career-intelligence", tags=["Career Intelligence"])

# Pydantic Models
class CareerProfileRequest(BaseModel):
    city: str = "Toronto"
    industry: str = "Tech"
    experience_level: str = "Junior"
    education: str = "Bachelor"
    python_skill: float = 5.0
    sql_skill: float = 5.0
    ml_skill: float = 3.0
    communication_skill: float = 6.0
    portfolio_projects: int = 2
    github_commits: int = 50
    years_experience: float = 2.0

class CareerAnalysisResponse(BaseModel):
    predictions: Dict[str, Any]
    scores: Dict[str, float]
    recommendations: List[Dict[str, Any]]
    career_pathway: Dict[str, Any]
    market_analysis: Dict[str, Any]
    timestamp: str
    
class ModelTrainingResponse(BaseModel):
    training_status: str
    model_scores: Dict[str, float]
    training_time: str
    timestamp: str

@router.post("/analyze", response_model=CareerAnalysisResponse)
async def analyze_career_profile(profile: CareerProfileRequest):
    """
    🎯 COMPREHENSIVE CAREER ANALYSIS
    
    Level 1 Features:
    - Salary prediction using ML models
    - Job match probability calculation
    - Skill gap analysis with recommendations
    - Career growth index modeling
    
    Level 2 Features:
    - Advanced statistical analysis
    - Market positioning insights
    - Portfolio strength assessment
    - Interactive visualization data
    """
    try:
        logger.info(f"🚀 Starting career analysis for profile: {profile.city}, {profile.industry}")
        
        # Convert Pydantic model to dict
        profile_dict = profile.dict()
        
        # Generate comprehensive career insights
        insights = await career_engine.generate_career_insights(profile_dict)
        
        logger.info("✅ Career analysis completed successfully")
        return CareerAnalysisResponse(**insights)
        
    except Exception as e:
        logger.error(f"❌ Error in career analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Career analysis failed: {str(e)}")

@router.post("/dashboard/{profile_id}")
async def generate_career_dashboard(profile_id: str, profile: CareerProfileRequest):
    """
    📊 INTERACTIVE CAREER DASHBOARD
    
    Generate comprehensive interactive dashboard with:
    - Real-time career metrics
    - Salary benchmarking charts
    - Skills radar visualization
    - Market positioning analysis
    - Career pathway funnel
    - Portfolio strength indicators
    """
    try:
        logger.info(f"📊 Generating career dashboard for profile: {profile_id}")
        
        profile_dict = profile.dict()
        
        # Generate interactive dashboard HTML
        dashboard_html = await career_engine.create_career_dashboard(profile_dict)
        
        return {
            "profile_id": profile_id,
            "dashboard_html": dashboard_html,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")

@router.post("/train-models", response_model=ModelTrainingResponse)
async def train_career_models(background_tasks: BackgroundTasks):
    """
    🤖 TRAIN MACHINE LEARNING MODELS
    
    Train career prediction models:
    - Salary prediction (Gradient Boosting)
    - Job match probability (Random Forest)
    - Career level classification (Random Forest)
    """
    try:
        logger.info("🤖 Starting model training process...")
        start_time = datetime.now()
        
        # Train models
        scores = await career_engine.train_models()
        
        training_time = str(datetime.now() - start_time)
        
        return ModelTrainingResponse(
            training_status="completed",
            model_scores=scores,
            training_time=training_time,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Error training models: {e}")
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

@router.get("/metrics/{profile_id}")
async def get_career_metrics(
    city: str = "Toronto",
    industry: str = "Tech", 
    experience_level: str = "Junior",
    education: str = "Bachelor",
    python_skill: float = 5.0,
    sql_skill: float = 5.0,
    ml_skill: float = 3.0,
    communication_skill: float = 6.0,
    portfolio_projects: int = 2,
    github_commits: int = 50,
    years_experience: float = 2.0
):
    """
    🎯 QUICK CAREER METRICS
    Fast endpoint for real-time career scoring
    """
    try:
        profile = {
            'city': city,
            'industry': industry,
            'experience_level': experience_level,
            'education': education,
            'python_skill': python_skill,
            'sql_skill': sql_skill,
            'ml_skill': ml_skill,
            'communication_skill': communication_skill,
            'portfolio_projects': portfolio_projects,
            'github_commits': github_commits,
            'years_experience': years_experience
        }
        
        metrics = await career_engine.predict_career_metrics(profile)
        
        return {
            "job_market_score": metrics.job_market_score,
            "skill_gap_score": metrics.skill_gap_score,
            "salary_prediction": metrics.salary_prediction,
            "job_match_probability": metrics.job_match_probability,
            "career_growth_index": metrics.career_growth_index,
            "portfolio_strength": metrics.portfolio_strength,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting career metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Metrics calculation failed: {str(e)}")

@router.get("/market-analysis/{city}/{industry}")
async def get_market_analysis(city: str, industry: str):
    """
    📈 MARKET INTELLIGENCE
    Get comprehensive market analysis for specific city and industry
    """
    try:
        # Sample profile for market analysis
        sample_profile = {
            'city': city,
            'industry': industry,
            'experience_level': 'Intermediate',
            'education': 'Bachelor',
            'python_skill': 6.0,
            'sql_skill': 6.0,
            'ml_skill': 4.0,
            'communication_skill': 7.0,
            'portfolio_projects': 3,
            'github_commits': 100,
            'years_experience': 3.0
        }
        
        insights = await career_engine.generate_career_insights(sample_profile)
        market_analysis = insights['market_analysis']
        
        return {
            "city": city,
            "industry": industry,
            "market_data": market_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting market analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Market analysis failed: {str(e)}")

@router.get("/skill-recommendations")
async def get_skill_recommendations(
    current_python: float = 5.0,
    current_sql: float = 5.0,
    current_ml: float = 3.0,
    current_communication: float = 6.0,
    target_role: str = "Data Scientist"
):
    """
    🚀 PERSONALIZED SKILL RECOMMENDATIONS
    Get AI-powered skill development recommendations
    """
    try:
        profile = {
            'python_skill': current_python,
            'sql_skill': current_sql,
            'ml_skill': current_ml,
            'communication_skill': current_communication,
            'experience_level': 'Intermediate',
            'industry': 'Tech',
            'city': 'Toronto',
            'education': 'Bachelor',
            'portfolio_projects': 2,
            'github_commits': 50,
            'years_experience': 3.0
        }
        
        insights = await career_engine.generate_career_insights(profile)
        
        return {
            "target_role": target_role,
            "skill_recommendations": insights['recommendations'],
            "current_skill_gap_score": insights['scores']['skill_gap_score'],
            "improvement_timeline": "3-6 months for significant improvement",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting skill recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Skill analysis failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for Career Intelligence API"""
    return {
        "status": "healthy",
        "engine_trained": career_engine.is_trained,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "features": [
            "Career Prediction Models",
            "Interactive Dashboards", 
            "Market Intelligence",
            "Skill Gap Analysis",
            "Portfolio Assessment"
        ]
    }
