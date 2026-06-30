from dataclasses import dataclass


@dataclass(slots=True)
class ProjectProgress:
    total: int

    completed: int

    remaining: int

    percentage: float
