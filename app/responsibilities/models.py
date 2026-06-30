from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from app.services.time_service import TimeService


class ResponsibilityStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ResponsibilityPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class Responsibility:
    """
    Represents something the user is responsible for.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    title: str = ""

    description: str = ""

    status: ResponsibilityStatus = ResponsibilityStatus.TODO

    priority: ResponsibilityPriority = ResponsibilityPriority.MEDIUM

    due_date: datetime | None = None

    created_at: datetime = field(default_factory=TimeService.now)

    completed_at: datetime | None = None