"""
Crew API Routes - FastAPI Implementation for CrewAI
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from src.crews.workflow_crew import WorkflowCrew

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class CrewExecutionRequest(BaseModel):
    crew_type: str
    inputs: Dict[str, Any]
    priority: str = "medium"
    async_execution: bool = False

class CrewResponse(BaseModel):
    crew_id: str
    crew_type: str
    status: str
    result: Optional[Dict[str, Any]] = None
    execution_time: Optional[str] = None
    timestamp: str

# Global crews
active_crews = {}

@router.get("/list")
async def list_crews():
    """List all available CrewAI crews"""
    try:
        crews = [
            {
                "crew_type": "workflow_crew",
                "description": "Multi-agent crew for workflow management",
                "agents": ["workflow_agent", "analysis_agent", "execution_agent"],
                "process": "sequential",
                "status": "available"
            }
        ]
        
        return {
            "crews": crews,
            "total": len(crews),
            "framework": "CrewAI",
            "active_crews": len(active_crews)
        }
        
    except Exception as e:
        logger.error(f"Error listing crews: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", response_model=CrewResponse)
async def execute_crew(request: CrewExecutionRequest, background_tasks: BackgroundTasks):
    """Execute a CrewAI crew with given inputs"""
    try:
        crew_id = f"crew_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if request.crew_type == "workflow_crew":
            workflow_crew = WorkflowCrew()
            
            if request.async_execution:
                # Execute in background
                background_tasks.add_task(execute_crew_background, crew_id, workflow_crew, request.inputs)
                
                active_crews[crew_id] = {
                    "crew_type": request.crew_type,
                    "status": "running",
                    "started_at": datetime.now().isoformat()
                }
                
                return CrewResponse(
                    crew_id=crew_id,
                    crew_type=request.crew_type,
                    status="started",
                    timestamp=datetime.now().isoformat()
                )
            else:
                # Execute synchronously
                result = workflow_crew.execute_workflow_management(request.inputs)
                
                return CrewResponse(
                    crew_id=crew_id,
                    crew_type=request.crew_type,
                    status=result["status"],
                    result=result,
                    execution_time=result.get("execution_time"),
                    timestamp=datetime.now().isoformat()
                )
        else:
            raise HTTPException(status_code=400, detail="Invalid crew type")
            
    except Exception as e:
        logger.error(f"Error executing crew: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{crew_id}")
async def get_crew_execution_status(crew_id: str):
    """Get execution status of a specific crew"""
    try:
        if crew_id not in active_crews:
            raise HTTPException(status_code=404, detail="Crew execution not found")
        
        crew_info = active_crews[crew_id]
        
        # Add current timestamp for status check
        crew_info["last_checked"] = datetime.now().isoformat()
        
        return crew_info
        
    except Exception as e:
        logger.error(f"Error getting crew status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/active")
async def get_active_crews():
    """Get all currently active crew executions"""
    try:
        return {
            "active_crews": active_crews,
            "total_active": len(active_crews),
            "framework": "CrewAI",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting active crews: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop/{crew_id}")
async def stop_crew_execution(crew_id: str):
    """Stop a running crew execution"""
    try:
        if crew_id not in active_crews:
            raise HTTPException(status_code=404, detail="Crew execution not found")
        
        # Update status to stopped
        active_crews[crew_id]["status"] = "stopped"
        active_crews[crew_id]["stopped_at"] = datetime.now().isoformat()
        
        logger.info(f"Crew execution stopped: {crew_id}")
        
        return {
            "crew_id": crew_id,
            "status": "stopped",
            "message": "Crew execution stopped successfully"
        }
        
    except Exception as e:
        logger.error(f"Error stopping crew: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{crew_id}")
async def delete_crew_execution(crew_id: str):
    """Delete a crew execution record"""
    try:
        if crew_id not in active_crews:
            raise HTTPException(status_code=404, detail="Crew execution not found")
        
        del active_crews[crew_id]
        
        logger.info(f"Crew execution deleted: {crew_id}")
        
        return {
            "crew_id": crew_id,
            "status": "deleted",
            "message": "Crew execution record deleted"
        }
        
    except Exception as e:
        logger.error(f"Error deleting crew execution: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def execute_crew_background(crew_id: str, workflow_crew: WorkflowCrew, inputs: Dict[str, Any]):
    """Background task for crew execution"""
    try:
        logger.info(f"Background crew execution started: {crew_id}")
        
        # Update status
        active_crews[crew_id]["status"] = "executing"
        
        # Execute the crew
        result = workflow_crew.execute_workflow_management(inputs)
        
        # Update with results
        active_crews[crew_id].update({
            "status": "completed",
            "result": result,
            "completed_at": datetime.now().isoformat()
        })
        
        logger.info(f"Background crew execution completed: {crew_id}")
        
    except Exception as e:
        logger.error(f"Error in background crew execution: {str(e)}")
        active_crews[crew_id].update({
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        })

@router.get("/metrics")
async def get_crew_metrics():
    """Get crew execution metrics and statistics"""
    try:
        completed_crews = [c for c in active_crews.values() if c["status"] == "completed"]
        failed_crews = [c for c in active_crews.values() if c["status"] == "failed"]
        running_crews = [c for c in active_crews.values() if c["status"] in ["running", "executing"]]
        
        metrics = {
            "total_executions": len(active_crews),
            "completed": len(completed_crews),
            "failed": len(failed_crews),
            "running": len(running_crews),
            "success_rate": len(completed_crews) / len(active_crews) * 100 if active_crews else 0,
            "framework": "CrewAI",
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting crew metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
