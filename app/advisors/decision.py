from enum import Enum
from dataclasses import dataclass, field

class DecisionOutcome(str, Enum):
    YES = "YES"
    NO = "NO"
    CONDITIONAL = "CONDITIONAL"

@dataclass(slots=True)
class AdvisorDecision:
    """
    Represents the result of an advisor's reasoning.
    """

    outcome: DecisionOutcome
    confidence: float
    reasoning: list[str] = field(default_factory=list)
