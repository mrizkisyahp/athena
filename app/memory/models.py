from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from app.services.time_service import TimeService


class MemoryType(str, Enum):
    """Enumeration of possible memory categories."""
    PREFERENCE = "preference"
    GOAL = "goal"
    ROUTINE = "routine"
    CONTEXT = "context"


class MemoryImportance(str, Enum):
    """Enumeration of memory priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class Memory:
    """
    Represents a single long-lived fact or piece of information in Athena's memory.
    """
    memory_type: MemoryType
    content: str
    importance: MemoryImportance
    
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=TimeService.now)
