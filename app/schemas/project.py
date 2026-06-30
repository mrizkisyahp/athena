from pydantic import BaseModel
from datetime import datetime
from app.schemas.task import TaskResponse


class ProjectRequest(BaseModel):
    name: str
    description: str = ""


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime


class ProjectProgressResponse(BaseModel):
    total: int
    completed: int
    remaining: int
    percentage: float


class ProjectOverviewResponse(BaseModel):
    project: ProjectResponse
    progress: ProjectProgressResponse
    responsibilities: list[TaskResponse]
