from app.database.models import ResponsibilityORM, ProjectORM, MemoryORM
from app.responsibilities.models import Responsibility
from app.projects.models import Project
from app.memory.models import Memory, MemoryType, MemoryImportance
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

def to_memory_domain(model: MemoryORM) -> Memory:
    return Memory(
        id=model.id,
        memory_type=MemoryType(model.memory_type),
        content=model.content,
        importance=MemoryImportance(model.importance),
        created_at=model.created_at,
    )

def to_memory_orm(domain_model: Memory) -> MemoryORM:
    return MemoryORM(
        id=domain_model.id,
        memory_type=domain_model.memory_type.value,
        content=domain_model.content,
        importance=domain_model.importance.value,
        created_at=domain_model.created_at
    )

from app.calendar.models import Event
from app.database.models import EventORM

def to_event_domain(orm_model: EventORM) -> Event:
    return Event(
        id=orm_model.id,
        title=orm_model.title,
        start_time=orm_model.start_time,
        end_time=orm_model.end_time,
        location=orm_model.location,
        notes=orm_model.notes,
        created_at=orm_model.created_at
    )

def to_event_orm(domain_model: Event) -> EventORM:
    return EventORM(
        id=domain_model.id,
        title=domain_model.title,
        start_time=domain_model.start_time,
        end_time=domain_model.end_time,
        location=domain_model.location,
        notes=domain_model.notes,
        created_at=domain_model.created_at
    )
