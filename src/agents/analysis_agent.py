"""
Analysis and Planning Agent - CrewAI Implementation
"""

from crewai import Agent
# Temporarily remove tool imports to fix startup
# from src.tools.analysis_tools import analyze_data, generate_insights, create_reports, forecast_trends
import logging

logger = logging.getLogger(__name__)

class AnalysisAgent:
    """Agent responsible for data analysis and strategic planning"""
    
    @staticmethod
    def create_agent() -> Agent:
        """Create a CrewAI analysis agent"""
        
        agent = Agent(
            role="Strategic Analyst",
            goal="Analyze data, identify patterns, and provide strategic insights for workflow optimization",
            backstory="""You are a brilliant data analyst and strategic planner with expertise 
            in business intelligence. You excel at processing large amounts of information, 
            identifying trends and patterns, and translating insights into actionable 
            recommendations for workflow improvement.""",
            
            tools=[
                # Temporarily empty tools list to fix startup
                # analyze_data,
                # generate_insights,
                # create_reports,
                # forecast_trends
            ],
            
            verbose=True,
            allow_delegation=False,
            
            # CrewAI specific configurations
            max_iter=15,
            memory=True
        )
        
        logger.info("Analysis Agent created successfully")
        return agent

    @staticmethod
    def get_agent_config() -> dict:
        """Return agent configuration for debugging"""
        return {
            "type": "analysis_agent",
            "role": "Strategic Analyst",
            "capabilities": [
                "data_analysis",
                "pattern_recognition",
                "trend_forecasting",
                "report_generation"
            ],
            "tools_count": 4,
            "delegation_enabled": False
        }
