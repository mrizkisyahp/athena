from app.responsibilities.models import Responsibility
from app.schemas.task import TaskResponse


def to_task_response(
    responsibility: Responsibility,
) -> TaskResponse:
    duration_minutes = responsibility.estimated_duration.minutes if responsibility.estimated_duration else None
    return TaskResponse(
        id=responsibility.id,
        title=responsibility.title,
        description=responsibility.description,
        status=responsibility.status,
        priority=responsibility.priority,
        due_date=responsibility.due_date,
        created_at=responsibility.created_at,
        completed_at=responsibility.completed_at,
        project_id=responsibility.project_id,
        estimated_duration_minutes=duration_minutes,
    )
