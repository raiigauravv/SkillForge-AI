"""
Workflow Tasks for CrewAI Implementation
"""

from crewai import Task
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WorkflowTasks:
    """Tasks for workflow management and execution"""
    
    def workflow_analysis_task(self) -> Task:
        """Task for analyzing workflow requirements"""
        return Task(
            description="""
            Analyze the provided workflow requirements and constraints.
            
            Your analysis should include:
            1. Requirements breakdown and clarification
            2. Stakeholder analysis and needs assessment
            3. Constraint identification and impact analysis
            4. Resource requirement estimation
            5. Risk assessment and mitigation strategies
            
            Provide a comprehensive analysis report with actionable insights.
            """,
            
            expected_output="""
            A detailed analysis report containing:
            - Requirements summary and breakdown
            - Stakeholder needs and expectations
            - Identified constraints and limitations
            - Resource requirements and estimates
            - Risk assessment with mitigation strategies
            - Recommendations for workflow design
            """,
            
            # Task configuration
            human_input=False       # No human input required
        )
    
    def workflow_design_task(self) -> Task:
        """Task for designing the workflow structure"""
        return Task(
            description="""
            Based on the analysis results, design an optimal workflow structure.
            
            Your design should include:
            1. Workflow step definition and sequencing
            2. Agent role assignments and responsibilities
            3. Data flow and dependency mapping
            4. Error handling and recovery procedures
            5. Performance optimization opportunities
            6. Monitoring and feedback mechanisms
            
            Create a detailed workflow blueprint ready for implementation.
            """,
            
            expected_output="""
            A comprehensive workflow design document containing:
            - Step-by-step workflow structure
            - Agent assignments and responsibilities
            - Data flow diagrams and dependencies
            - Error handling procedures
            - Performance optimization plan
            - Monitoring and metrics framework
            """,
            
            # Task configuration
            human_input=False
        )
    
    def workflow_execution_task(self) -> Task:
        """Task for executing the designed workflow"""
        return Task(
            description="""
            Execute the designed workflow according to the specifications.
            
            Your execution should include:
            1. Workflow implementation and deployment
            2. Step-by-step execution monitoring
            3. Real-time performance tracking
            4. Error detection and handling
            5. Quality assurance and validation
            6. Progress reporting and updates
            
            Ensure reliable and efficient workflow execution.
            """,
            
            expected_output="""
            A workflow execution report containing:
            - Execution status and progress
            - Performance metrics and statistics
            - Error reports and resolutions
            - Quality assurance results
            - Resource utilization data
            - Completion summary and outcomes
            """,
            
            # Task configuration
            human_input=False
        )
    
    def workflow_monitoring_task(self) -> Task:
        """Task for monitoring and optimizing workflow performance"""
        return Task(
            description="""
            Monitor the executed workflow and provide optimization recommendations.
            
            Your monitoring should include:
            1. Performance metrics analysis
            2. Efficiency and bottleneck identification
            3. Quality assessment and improvements
            4. Cost-benefit analysis
            5. Optimization recommendations
            6. Future enhancement suggestions
            
            Provide actionable insights for continuous improvement.
            """,
            
            expected_output="""
            A workflow monitoring and optimization report containing:
            - Performance analysis and metrics
            - Identified bottlenecks and inefficiencies
            - Quality assessment results
            - Cost-benefit analysis
            - Optimization recommendations
            - Future enhancement roadmap
            """,
            
            # Task configuration
            human_input=False
        )
    
    def get_task_definitions(self) -> Dict[str, Any]:
        """Return all task definitions for reference"""
        return {
            "workflow_analysis": {
                "purpose": "Analyze workflow requirements",
                "expected_duration": "5 minutes",
                "dependencies": None
            },
            "workflow_design": {
                "purpose": "Design workflow structure",
                "expected_duration": "10 minutes", 
                "dependencies": ["workflow_analysis"]
            },
            "workflow_execution": {
                "purpose": "Execute designed workflow",
                "expected_duration": "20 minutes",
                "dependencies": ["workflow_design"]
            },
            "workflow_monitoring": {
                "purpose": "Monitor and optimize workflow",
                "expected_duration": "5 minutes",
                "dependencies": ["workflow_execution"]
            }
        }
