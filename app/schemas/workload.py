from pydantic import BaseModel


class WorkloadRequest(BaseModel):
    available_minutes: int


class WorkloadResponse(BaseModel):
    recommendation: str
