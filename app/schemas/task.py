from datetime import datetime

from pydantic import BaseModel

from app.responsibilities.models import (
    ResponsibilityPriority,
    ResponsibilityStatus,
)


class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""
    priority: ResponsibilityPriority = ResponsibilityPriority.MEDIUM
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: ResponsibilityStatus
    priority: ResponsibilityPriority
    due_date: datetime | None
    created_at: datetime
    completed_at: datetime | None