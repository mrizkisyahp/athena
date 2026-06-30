from app.database.models import ResponsibilityORM
from app.responsibilities.models import Responsibility


def to_domain(model: ResponsibilityORM) -> Responsibility:
    return Responsibility(
        id=model.id,
        title=model.title,
        description=model.description,
        status=model.status,
        priority=model.priority,
        due_date=model.due_date,
        created_at=model.created_at,
        completed_at=model.completed_at,
    )


def to_orm(model: Responsibility) -> ResponsibilityORM:
    return ResponsibilityORM(
        id=model.id,
        title=model.title,
        description=model.description,
        status=model.status,
        priority=model.priority,
        due_date=model.due_date,
        created_at=model.created_at,
        completed_at=model.completed_at,
    )
