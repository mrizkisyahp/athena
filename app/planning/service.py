from typing import Any
from datetime import datetime
from app.responsibilities.models import Responsibility, ResponsibilityPriority
from app.responsibilities.service import ResponsibilityService
from app.planning.models import ExecutionPlan
from app.services.time_service import TimeService

_PRIORITY_ORDER = {
    ResponsibilityPriority.CRITICAL: 0,
    ResponsibilityPriority.HIGH: 1,
    ResponsibilityPriority.MEDIUM: 2,
    ResponsibilityPriority.LOW: 3,
}

class ExecutionPlanner:

    def __init__(
        self,
        responsibility_service: ResponsibilityService,
    ):
        self._responsibility_service = responsibility_service

    def _due_status(self, responsibility: Responsibility, now: datetime) -> int:
        if not responsibility.due_date:
            return 3 # No due date (last)
            
        if responsibility.due_date < now:
            return 0 # Overdue
            
        # Due today (same calendar day as now, or within 24h?)
        # Let's say if due date date is same as now date
        # But `now` has time. We can just check if due_date is on the same calendar day.
        # Actually, let's just check if it's <= end of today.
        end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        if responsibility.due_date <= end_of_today:
            return 1 # Today
            
        return 2 # Future

    def _sort_key(self, responsibility: Responsibility) -> tuple:
        now = TimeService.now()
        
        # Rule 1 & Due Status bucket
        sort_due_status = self._due_status(responsibility, now)
        
        # Rule 2: Priority
        sort_priority = _PRIORITY_ORDER.get(responsibility.priority, 99)
        
        # Rule 3: Earlier due dates
        sort_due_date = responsibility.due_date.timestamp() if responsibility.due_date else float('inf')
        
        # Rule 4: Older responsibilities first
        sort_created = responsibility.created_at.timestamp()
        
        return (
            sort_due_status,
            sort_priority,
            sort_due_date,
            sort_created,
        )

    def generate_plan(self) -> ExecutionPlan:
        responsibilities = self._responsibility_service.get_all()
        
        # Filter out completed tasks
        from app.responsibilities.models import ResponsibilityStatus
        pending = [
            r for r in responsibilities 
            if r.status != ResponsibilityStatus.COMPLETED
        ]

        ordered = sorted(
            pending,
            key=self._sort_key,
        )

        rationale = [
            "Overdue responsibilities are scheduled before future work.",
            "Higher-priority responsibilities are scheduled first.",
            "Earlier deadlines take precedence when priorities are equal.",
        ]

        return ExecutionPlan(
            responsibilities=ordered,
            rationale=rationale,
        )
