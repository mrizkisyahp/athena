from datetime import datetime
from sqlalchemy import select

from app.responsibilities.models import (
    Responsibility,
    ResponsibilityStatus,
    ResponsibilityPriority,
)
from app.time.duration import Duration
from app.services.time_service import TimeService
from app.database.session import SessionLocal
from app.database.models import ResponsibilityORM
from app.database.mappers import to_domain, to_orm


class ResponsibilityService:
    """
    Manages the user's responsibilities.
    """

    def __init__(self):
        self._session_factory = SessionLocal

    def add(self, responsibility: Responsibility) -> Responsibility:
        with self._session_factory() as session:
            orm = to_orm(responsibility)
            session.add(orm)
            session.commit()
        return responsibility

    def create(
        self,
        title: str,
        description: str = "",
        priority: ResponsibilityPriority = ResponsibilityPriority.MEDIUM,
        due_date: datetime | None = None,
        project_id: str | None = None,
        estimated_duration: Duration | None = None,
    ) -> Responsibility:
        responsibility = Responsibility(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            project_id=project_id,
            estimated_duration=estimated_duration,
        )
        self.add(responsibility)
        return responsibility

    def get_all(self) -> list[Responsibility]:
        with self._session_factory() as session:
            rows = session.scalars(select(ResponsibilityORM)).all()
        return [to_domain(row) for row in rows]

    def get_by_id(self, responsibility_id: str) -> Responsibility | None:
        with self._session_factory() as session:
            row = session.scalar(
                select(ResponsibilityORM).where(ResponsibilityORM.id == responsibility_id)
            )
            if row is None:
                return None
            return to_domain(row)

    def complete(self, responsibility_id: str) -> Responsibility | None:
        with self._session_factory() as session:
            row = session.scalar(
                select(ResponsibilityORM).where(ResponsibilityORM.id == responsibility_id)
            )
            if row is None:
                return None
            
            row.status = ResponsibilityStatus.COMPLETED
            row.completed_at = TimeService.now()
            session.commit()
            return to_domain(row)

    def get_due_today(self) -> list[Responsibility]:
        """
        Returns all incomplete responsibilities due today.
        """
        today = TimeService.now().date()
        return [
            responsibility
            for responsibility in self.get_all()
            if (
                responsibility.due_date is not None
                and responsibility.due_date.date() == today
                and responsibility.status != ResponsibilityStatus.COMPLETED
            )
        ]

    def get_high_priority_today(self) -> list[Responsibility]:
        """
        Returns today's HIGH and CRITICAL responsibilities.
        """
        return [
            responsibility
            for responsibility in self.get_due_today()
            if responsibility.priority in (
                ResponsibilityPriority.HIGH,
                ResponsibilityPriority.CRITICAL,
            )
        ]

    def get_overdue(self) -> list[Responsibility]:
        """
        Returns all incomplete overdue responsibilities.
        """
        today = TimeService.now().date()
        return [
            responsibility
            for responsibility in self.get_all()
            if (
                responsibility.due_date is not None
                and responsibility.due_date.date() < today
                and responsibility.status != ResponsibilityStatus.COMPLETED
            )
        ]

    def get_completed_today(self) -> list[Responsibility]:
        """
        Returns responsibilities completed today.
        """
        today = TimeService.now().date()
        return [
            responsibility
            for responsibility in self.get_all()
            if (
                responsibility.completed_at is not None
                and responsibility.completed_at.date() == today
            )
        ]