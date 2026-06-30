from datetime import datetime

from app.responsibilities.models import (
    Responsibility,
    ResponsibilityStatus,
    ResponsibilityPriority,
)
from app.services.time_service import TimeService


class ResponsibilityService:
    """
    Manages the user's responsibilities.
    """

    def __init__(self):
        self._responsibilities: list[Responsibility] = []

    def add(self, responsibility: Responsibility) -> Responsibility:
        self._responsibilities.append(responsibility)
        return responsibility

    def create(
        self,
        title: str,
        description: str = "",
        priority: ResponsibilityPriority = ResponsibilityPriority.MEDIUM,
        due_date: datetime | None = None,
    ) -> Responsibility:
        responsibility = Responsibility(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        self.add(responsibility)
        return responsibility

    def get_all(self) -> list[Responsibility]:
        return self._responsibilities.copy()

    def get_by_id(self, responsibility_id: str) -> Responsibility | None:
        for responsibility in self._responsibilities:
            if responsibility.id == responsibility_id:
                return responsibility

        return None

    def complete(self, responsibility_id: str) -> Responsibility | None:
        responsibility = self.get_by_id(responsibility_id)

        if responsibility is None:
            return None

        responsibility.status = ResponsibilityStatus.COMPLETED
        responsibility.completed_at = TimeService.now()

        return responsibility

    def clear(self) -> None:
        self._responsibilities.clear()

    def get_due_today(self) -> list[Responsibility]:
        """
        Returns all incomplete responsibilities due today.
        """

        today = TimeService.now().date()

        return [
            responsibility
            for responsibility in self._responsibilities
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
            for responsibility in self._responsibilities
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
            for responsibility in self._responsibilities
            if (
                responsibility.completed_at is not None
                and responsibility.completed_at.date() == today
            )
        ]