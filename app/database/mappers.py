from app.database.models import ResponsibilityORM, ProjectORM
from app.responsibilities.models import Responsibility
from app.projects.models import Project
from app.time.duration import Duration


def to_domain(model: ResponsibilityORM) -> Responsibility:
    duration = Duration(model.estimated_duration_minutes) if model.estimated_duration_minutes is not None else None
    return Responsibility(
        id=model.id,
        title=model.title,
        description=model.description,
        status=model.status,
        priority=model.priority,
        due_date=model.due_date,
        created_at=model.created_at,
        completed_at=model.completed_at,
        project_id=model.project_id,
        estimated_duration=duration,
    )


def to_orm(model: Responsibility) -> ResponsibilityORM:
    duration_minutes = model.estimated_duration.minutes if model.estimated_duration else None
    return ResponsibilityORM(
        id=model.id,
        title=model.title,
        description=model.description,
        status=model.status,
        priority=model.priority,
        due_date=model.due_date,
        created_at=model.created_at,
        completed_at=model.completed_at,
        project_id=model.project_id,
        estimated_duration_minutes=duration_minutes,
    )

def to_project_domain(model: ProjectORM) -> Project:
    return Project(
        id=model.id,
        name=model.name,
        description=model.description,
        created_at=model.created_at,
    )

def to_project_orm(model: Project) -> ProjectORM:
    return ProjectORM(
        id=model.id,
        name=model.name,
        description=model.description,
        created_at=model.created_at,
    )
