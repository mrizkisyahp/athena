from datetime import date
from app.time.duration import Duration
from app.planning.service import ExecutionPlanner
from app.workload.service import WorkloadBalancer
from app.calendar.availability import AvailabilityEngine
from app.awareness.models import Insight, InsightSeverity

class InsightEngine:
    def __init__(
        self,
        planner: ExecutionPlanner,
        workload: WorkloadBalancer,
        availability: AvailabilityEngine,
    ):
        self._planner = planner
        self._workload = workload
        self._availability = availability

    def generate(self, day: date, available_capacity: Duration) -> list[Insight]:
        insights = []

        # Gather data from engines
        analysis = self._workload.analyze(available_capacity)
        schedule = self._planner.generate_schedule(day)
        avail = self._availability.calculate(day)
        
        # Safe extraction
        schedule_tasks = schedule.tasks if schedule else []
        unscheduled = schedule.unscheduled if schedule else []

        # Rule 1: Overloaded Day
        if analysis.overloaded:
            insights.append(Insight(
                title="Overloaded Day",
                description="Today's planned work exceeds your available capacity.",
                severity=InsightSeverity.HIGH
            ))

        # Rule 2: Empty Schedule
        if not schedule_tasks:
            insights.append(Insight(
                title="No Scheduled Work",
                description="No responsibilities are currently scheduled today.",
                severity=InsightSeverity.MEDIUM
            ))

        # Rule 3: Idle Capacity
        largest_block_minutes = max((block.duration.minutes for block in avail.free_blocks), default=0)
        if largest_block_minutes >= 120:
            insights.append(Insight(
                title="Large Focus Block Available",
                description="You have a large uninterrupted block available for deep work.",
                severity=InsightSeverity.LOW
            ))

        # Rule 4: Unscheduled Responsibilities
        if unscheduled:
            insights.append(Insight(
                title="Unscheduled Responsibilities",
                description="Some responsibilities could not be placed into today's schedule.",
                severity=InsightSeverity.HIGH
            ))

        # Sort: HIGH -> MEDIUM -> LOW
        severity_order = {
            InsightSeverity.HIGH: 0,
            InsightSeverity.MEDIUM: 1,
            InsightSeverity.LOW: 2
        }

        # Python's sorted is stable, so ordering within same severity is preserved
        return sorted(insights, key=lambda i: severity_order[i.severity])
