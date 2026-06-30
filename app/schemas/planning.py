from pydantic import BaseModel


class ExecutionPlanResponse(BaseModel):
    plan: str
