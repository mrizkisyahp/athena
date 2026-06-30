from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Duration:
    """
    Represents an estimated duration in minutes.
    """

    minutes: int

    def __post_init__(self):
        if self.minutes <= 0:
            raise ValueError(
                "Duration must be positive."
            )
            
    @property
    def hours(self) -> float:
        return self.minutes / 60

    def __str__(self):
        if self.minutes < 60:
            return f"{self.minutes} min"

        hours = self.minutes / 60

        return f"{hours:g} hr"
