from pydantic import BaseModel

from app.schemas.task import TaskResponse


class TodayResponse(BaseModel):
    today: list[TaskResponse]
    overdue: list[TaskResponse]
    completed_today: list[TaskResponse]
