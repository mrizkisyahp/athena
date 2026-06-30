from dataclasses import dataclass, field

from app.responsibilities.models import Responsibility


from app.time.duration import Duration


@dataclass(slots=True)
class ExecutionPlan:
    """
    Represents Athena's recommended execution order.
    """

    responsibilities: list[Responsibility] = field(default_factory=list)

    rationale: list[str] = field(default_factory=list)
    
    total_estimated_duration: Duration | None = None
