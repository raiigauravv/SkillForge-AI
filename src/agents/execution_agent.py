"""
Execution and Automation Agent - CrewAI Implementation
"""

from crewai import Agent
# Temporarily remove tool imports to fix startup
# from src.tools.execution_tools import execute_task, automate_process, schedule_task, monitor_tasks
import logging

logger = logging.getLogger(__name__)

class ExecutionAgent:
    """Agent responsible for executing tasks and automating processes"""
    
    @staticmethod
    def create_agent() -> Agent:
        """Create a CrewAI execution agent"""
        
        agent = Agent(
            role="Automation Specialist",
            goal="Execute workflows efficiently, automate repetitive tasks, and ensure reliable process completion",
            backstory="""You are a highly skilled automation specialist with extensive 
            experience in process execution and task automation. You excel at translating 
            plans into action, handling complex execution scenarios, and ensuring 
            robust and reliable task completion.""",
            
            tools=[
                # Temporarily empty tools list to fix startup
                # execute_task,
                # automate_process,
                # schedule_task,
                # monitor_tasks
            ],
            
            verbose=True,
            allow_delegation=False,
            
            # CrewAI specific configurations
            max_iter=20,
            memory=True
        )
        
        logger.info("Execution Agent created successfully")
        return agent

    @staticmethod
    def get_agent_config() -> dict:
        """Return agent configuration for debugging"""
        return {
            "type": "execution_agent",
            "role": "Automation Specialist",
            "capabilities": [
                "task_execution",
                "process_automation",
                "error_handling",
                "result_validation"
            ],
            "tools_count": 4,
            "delegation_enabled": False
        }
