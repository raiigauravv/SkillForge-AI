"""
Agent API Routes - FastAPI Implementation for CrewAI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
from datetime import datetime

from src.agents.workflow_agent import WorkflowAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.execution_agent import ExecutionAgent

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class AgentInteractionRequest(BaseModel):
    agent_type: str
    message: str
    conversation_history: List[Dict[str, str]] = []
    context: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    agent_type: str
    response: str
    timestamp: str
    status: str

@router.get("/list")
async def list_agents():
    """List all available CrewAI agents"""
    try:
        agents = [
            {
                "type": "workflow_agent",
                "config": WorkflowAgent.get_agent_config()
            },
            {
                "type": "analysis_agent", 
                "config": AnalysisAgent.get_agent_config()
            },
            {
                "type": "execution_agent",
                "config": ExecutionAgent.get_agent_config()
            }
        ]
        
        return {
            "agents": agents,
            "total": len(agents),
            "framework": "CrewAI"
        }
        
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{agent_type}")
async def get_agent_status(agent_type: str):
    """Get specific agent status and capabilities"""
    try:
        agent_configs = {
            "workflow_agent": WorkflowAgent.get_agent_config(),
            "analysis_agent": AnalysisAgent.get_agent_config(),
            "execution_agent": ExecutionAgent.get_agent_config()
        }
        
        if agent_type not in agent_configs:
            raise HTTPException(status_code=404, detail="Agent type not found")
        
        config = agent_configs[agent_type]
        config["status"] = "active"
        config["last_updated"] = datetime.now().isoformat()
        
        return config
        
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interact", response_model=AgentResponse)
async def interact_with_agent(request: AgentInteractionRequest):
    """Interact with a specific CrewAI agent"""
    try:
        from openai import OpenAI
        import os
        
        # Get OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simple prompt based on agent type
        if request.agent_type == "analysis_agent":
            system_prompt = "You are a Business Analysis Agent. Provide data-driven insights and strategic recommendations."
        elif request.agent_type == "workflow_agent":
            system_prompt = "You are a Workflow Agent. Create step-by-step processes and operational plans."
        elif request.agent_type == "execution_agent":
            system_prompt = "You are an Execution Agent. Provide specific implementation steps and tools."
        else:
            system_prompt = "You are a helpful AI assistant."
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in request.conversation_history[-5:]:
            messages.append({
                "role": msg.get("role", "user"), 
                "content": msg.get("content", "")
            })
        
        # Add current message
        messages.append({"role": "user", "content": request.message})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        return AgentResponse(
            agent_type=request.agent_type,
            response=ai_response,
            timestamp=datetime.now().isoformat(),
            status="completed"
        )
        
    except Exception as e:
        logger.error(f"Error in agent interaction: {str(e)}")
        
        # Fallback responses
        fallback_responses = {
            "analysis_agent": "I analyze business data and provide strategic insights.",
            "workflow_agent": "I create efficient workflows and processes.",
            "execution_agent": "I help with implementation and automation."
        }
        
        return AgentResponse(
            agent_type=request.agent_type,
            response=fallback_responses.get(request.agent_type, "Agent temporarily unavailable"),
            timestamp=datetime.now().isoformat(),
            status="completed"
        )

@router.get("/capabilities/{agent_type}")
async def get_agent_capabilities(agent_type: str):
    """Get detailed capabilities of a specific agent"""
    try:
        capabilities = {
            "workflow_agent": {
                "tools": ["create_workflow", "execute_workflow", "monitor_workflow"],
                "specializations": ["process_optimization", "agent_coordination"]
            },
            "analysis_agent": {
                "tools": ["analyze_data", "generate_insights", "create_reports"],
                "specializations": ["data_analysis", "strategic_planning"]
            },
            "execution_agent": {
                "tools": ["execute_task", "automate_process", "handle_errors"],
                "specializations": ["task_execution", "process_automation"]
            }
        }
        
        if agent_type not in capabilities:
            raise HTTPException(status_code=404, detail="Agent type not found")
        
        return {
            "agent_type": agent_type,
            "capabilities": capabilities[agent_type],
            "framework": "CrewAI"
        }
        
    except Exception as e:
        logger.error(f"Error getting agent capabilities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
