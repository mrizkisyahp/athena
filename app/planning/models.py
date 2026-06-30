from dataclasses import dataclass, field

from app.responsibilities.models import Responsibility


@dataclass(slots=True)
class ExecutionPlan:
    """
    Represents Athena's recommended execution order.
    """

    responsibilities: list[Responsibility] = field(default_factory=list)

    rationale: list[str] = field(default_factory=list)
