from pathlib import Path
from devtools.models import PipelineRequest, PipelineRun, Agent
from devtools.config import EngineeringTeam

class PipelineEngine:
    def __init__(self):
        self.prompts_dir = Path("devtools/prompts")
        
    def plan(self, request: PipelineRequest) -> PipelineRun:
        execution_order = [
            EngineeringTeam.ARCHITECT,
            EngineeringTeam.BACKEND_EXECUTOR,
        ]
        
        if request.touches_database:
            execution_order.append(EngineeringTeam.DATABASE_REVIEWER)
            
        execution_order.append(EngineeringTeam.QA_REVIEWER)
        
        return PipelineRun(
            name=request.title,
            planned_agents=execution_order,
            results=[]
        )
