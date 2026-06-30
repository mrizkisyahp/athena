from datetime import datetime, timezone

class TimeService:
    """
    Centralized service for time-related operations.
    """

    @staticmethod
    def now() -> datetime:
        """
        Returns the current timezone-aware datetime in the local timezone.
        """
        return datetime.now().astimezone()
