"""
Workflow Management Crew - CrewAI Implementation
"""

from crewai import Crew, Process, Task
from src.agents.workflow_agent import WorkflowAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.execution_agent import ExecutionAgent
import logging

logger = logging.getLogger(__name__)

class WorkflowCrew:
    """CrewAI crew for managing complete workflow operations"""
    
    def __init__(self):
        self.workflow_agent = WorkflowAgent.create_agent()
        self.analysis_agent = AnalysisAgent.create_agent()
        self.execution_agent = ExecutionAgent.create_agent()
        
    def create_tasks(self):
        """Create tasks with proper agent assignments"""
        
        # Analysis Task - assigned to Analysis Agent
        analysis_task = Task(
            description="""Analyze this specific business problem: {workflow_description}

Requirements: {requirements}
Priority: {priority}

Provide a SHORT analysis (max 200 words):
🎯 MAIN ISSUE: [1-2 sentences about the core problem]
👥 WHO'S AFFECTED: [Key people/departments impacted]
⚠️ TOP 3 CHALLENGES: [Biggest obstacles]
💰 RESOURCES NEEDED: [Budget/time estimate]
🔥 QUICK WINS: [What can be done immediately]

Be specific to THIS problem, not generic.""",
            
            expected_output="""A focused analysis (max 200 words) addressing the specific business problem with concrete insights and recommendations.""",
            
            agent=self.analysis_agent
        )
        
        # Design Task - assigned to Workflow Agent
        design_task = Task(
            description="""Create a simple solution for: {workflow_description}

Based on the analysis, design a PRACTICAL solution (max 150 words):
🔄 SOLUTION STEPS: [3-4 clear steps to solve this problem]
👤 WHO DOES WHAT: [Specific role assignments]
⏰ TIMELINE: [Realistic timeframe]
📊 SUCCESS METRICS: [How to measure success]

Focus on THIS specific problem, be actionable.""",
            
            expected_output="""A practical solution plan (max 150 words) with clear steps, roles, timeline, and success metrics.""",
            
            agent=self.workflow_agent
        )
        
        # Execution Task - assigned to Execution Agent
        execution_task = Task(
            description="""Create an action plan for: {workflow_description}

Provide immediate next steps (max 100 words):
🚀 THIS WEEK: [What to do in the next 7 days]
🛠️ TOOLS/RESOURCES: [Specific tools or help needed]
💰 COST ESTIMATE: [Realistic budget/investment needed]
📈 30-DAY GOAL: [Measurable target for first month]

Be specific and actionable for THIS problem.""",
            
            expected_output="""A concise action plan (max 100 words) with immediate steps, tools needed, costs, and 30-day goals.""",
            
            agent=self.execution_agent
        )
        
        # Monitoring Task - assigned back to Analysis Agent for optimization
        monitoring_task = Task(
            description="""Provide quick optimization tips for: {workflow_description}

Give rapid improvements (max 100 words):
⚡ QUICK FIXES: [2-3 things to improve immediately]
📊 TRACK THESE: [Key metrics to monitor]
🎯 3-MONTH GOAL: [Realistic target]
💡 PRO TIP: [One expert insight]

Focus on practical, measurable improvements.""",
            
            expected_output="""Brief optimization recommendations (max 100 words) with quick fixes, metrics, goals, and expert tips.""",
            
            agent=self.analysis_agent
        )
        
        return [analysis_task, design_task, execution_task, monitoring_task]
        
    def create_crew(self) -> Crew:
        """Create and configure the workflow management crew"""
        
        tasks = self.create_tasks()
        
        # Define the crew with agents and their tasks
        crew = Crew(
            agents=[
                self.workflow_agent,
                self.analysis_agent,
                self.execution_agent
            ],
            
            tasks=tasks,
            
            # CrewAI process configuration
            process=Process.sequential,  # Tasks executed in sequence
            memory=True,  # Enable crew memory
            
            # Verbose output for debugging
            verbose=True
        )
        
        logger.info("Workflow crew created successfully")
        return crew
    
    def execute_workflow_management(self, workflow_request: dict) -> dict:
        """Execute complete workflow management process"""
        try:
            crew = self.create_crew()
            
            # Prepare inputs for the crew
            inputs = {
                "workflow_description": workflow_request.get("description", ""),
                "requirements": workflow_request.get("requirements", []),
                "constraints": workflow_request.get("constraints", {}),
                "priority": workflow_request.get("priority", "medium"),
                "deadline": workflow_request.get("deadline", ""),
                "stakeholders": workflow_request.get("stakeholders", [])
            }
            
            # Execute the crew
            result = crew.kickoff(inputs=inputs)
            
            logger.info("Workflow management execution completed")
            
            return {
                "status": "completed",
                "result": result,
                "crew_usage": crew.usage_metrics,
                "execution_time": "Completed successfully"
            }
            
        except Exception as e:
            error_msg = f"Error in workflow management execution: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "result": None
            }
    
    def get_crew_status(self) -> dict:
        """Get current status of the crew and its agents"""
        return {
            "crew_type": "workflow_management",
            "agents": [
                self.workflow_agent.role,
                self.analysis_agent.role,
                self.execution_agent.role
            ],
            "process_type": "sequential",
            "memory_enabled": True,
            "cache_enabled": True,
            "status": "ready"
        }
    
    def _step_callback(self, step_output):
        """Callback function for monitoring crew execution steps"""
        logger.info(f"Crew step completed: {step_output}")
        # Here you could add custom monitoring, logging, or notification logic
