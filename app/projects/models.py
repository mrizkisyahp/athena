from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from app.services.time_service import TimeService


@dataclass(slots=True)
class Project:
    id: str = field(default_factory=lambda: str(uuid4()))

    name: str = ""

    description: str = ""

    created_at: datetime = field(default_factory=TimeService.now)
