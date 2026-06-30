from dataclasses import dataclass, field


@dataclass(slots=True)
class AdvisorDecision:
    """
    Represents the result of an advisor's reasoning.
    """

    decision: str

    confidence: str

    reasoning: list[str] = field(default_factory=list)
