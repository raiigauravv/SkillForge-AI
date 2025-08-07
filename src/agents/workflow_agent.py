"""
Workflow Management Agent - CrewAI Implementation
"""

from crewai import Agent
# Temporarily remove tool imports to fix startup
# from src.tools.workflow_tools import create_workflow, execute_workflow, monitor_progress, update_workflow
import logging

logger = logging.getLogger(__name__)

class WorkflowAgent:
    """Agent responsible for workflow management and orchestration"""
    
    @staticmethod
    def create_agent() -> Agent:
        """Create a CrewAI workflow management agent"""
        
        agent = Agent(
            role="Workflow Orchestrator",
            goal="Manage and coordinate complex multi-step workflows efficiently",
            backstory="""You are an expert workflow orchestrator with deep understanding 
            of business processes. You excel at breaking down complex tasks into manageable 
            steps, coordinating between different agents, and ensuring smooth execution 
            of automated workflows.""",
            
            tools=[
                # Temporarily empty tools list to fix startup
                # create_workflow,
                # execute_workflow,
                # monitor_progress,
                # update_workflow
            ],
            
            verbose=True,
            allow_delegation=True,
            
            # CrewAI specific configurations
            max_iter=10,
            memory=True
        )
        
        logger.info("Workflow Agent created successfully")
        return agent

    @staticmethod
    def get_agent_config() -> dict:
        """Return agent configuration for debugging"""
        return {
            "type": "workflow_agent",
            "role": "Workflow Orchestrator",
            "capabilities": [
                "workflow_creation",
                "process_optimization",
                "agent_coordination",
                "execution_monitoring"
            ],
            "tools_count": 4,
            "delegation_enabled": True
        }
