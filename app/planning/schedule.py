from dataclasses import dataclass
from datetime import datetime
from app.responsibilities.models import Responsibility

@dataclass(frozen=True, slots=True)
class ScheduledTask:
    responsibility: Responsibility
    start_time: datetime
    end_time: datetime

@dataclass(frozen=True, slots=True)
class DailySchedule:
    tasks: list[ScheduledTask]
    unscheduled: list[Responsibility]
