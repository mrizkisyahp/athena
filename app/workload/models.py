from dataclasses import dataclass, field

from app.responsibilities.models import Responsibility
from app.time.duration import Duration


@dataclass(slots=True)
class WorkloadAnalysis:
    """
    Athena's deterministic assessment of today's workload.
    """

    total_workload: Duration | None

    available_capacity: Duration | None

    overloaded: bool

    suggested_deferrals: list[Responsibility] = field(default_factory=list)

    reasoning: list[str] = field(default_factory=list)
