from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from app.services.time_service import TimeService

class InsightSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass(frozen=True, slots=True)
class Insight:
    """
    Represents a deterministic observation produced by Athena.
    """
    title: str
    description: str
    severity: InsightSeverity
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=TimeService.now)

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Insight title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Insight description cannot be empty.")
