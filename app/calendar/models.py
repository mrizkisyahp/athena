from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from app.services.time_service import TimeService


@dataclass(frozen=True, slots=True)
class Event:
    """
    Represents a fixed commitment in the user's calendar.
    """

    title: str
    start_time: datetime
    end_time: datetime
    location: str | None = None
    notes: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=TimeService.now)

    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError(
                "Event end_time must be after start_time."
            )
