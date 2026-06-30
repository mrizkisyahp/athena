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

    def _group_projects(self, ordered: list[Responsibility], now: datetime) -> list[Responsibility]:
        if not ordered:
            return []

        result = []
        
        def get_tie_key(r: Responsibility) -> tuple:
            return (
                self._due_status(r, now),
                _PRIORITY_ORDER.get(r.priority, 99),
                r.due_date.timestamp() if r.due_date else float('inf')
            )
            
        current_group = []
        current_key = get_tie_key(ordered[0])
        
        for r in ordered:
            key = get_tie_key(r)
            if key == current_key:
                current_group.append(r)
            else:
                result.extend(self._cluster_group(current_group))
                current_group = [r]
                current_key = key
                
        if current_group:
            result.extend(self._cluster_group(current_group))
            
        return result

    def _cluster_group(self, group: list[Responsibility]) -> list[Responsibility]:
        placed = set()
        clustered = []
        
        for i, r in enumerate(group):
            if i in placed:
                continue
            
            clustered.append(r)
            placed.add(i)
            
            if r.project_id:
                for j, other_r in enumerate(group[i+1:], start=i+1):
                    if j not in placed and other_r.project_id == r.project_id:
                        clustered.append(other_r)
                        placed.add(j)
                        
        return clustered

    def generate_plan(self) -> ExecutionPlan:
        responsibilities = self._responsibility_service.get_all()
        now = TimeService.now()
        
        from app.responsibilities.models import ResponsibilityStatus
        pending = [
            r for r in responsibilities 
            if r.status != ResponsibilityStatus.COMPLETED
        ]

        # Phase 1: Hard Constraints
        ordered = sorted(
            pending,
            key=self._sort_key,
        )
        
        # Phase 2: Optimization
        ordered = self._group_projects(ordered, now)

        rationale = [
            "Overdue responsibilities are scheduled before future work.",
            "Higher-priority responsibilities are scheduled first.",
            "Earlier deadlines take precedence when priorities are equal.",
            "Related work is grouped together when possible to reduce context switching.",
        ]

        return ExecutionPlan(
            responsibilities=ordered,
            rationale=rationale,
        )
