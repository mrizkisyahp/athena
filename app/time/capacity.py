from dataclasses import dataclass
from app.time.duration import Duration

@dataclass(frozen=True, slots=True)
class CapacityRequest:
    available_time: Duration
