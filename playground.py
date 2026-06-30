from datetime import timedelta
from app.planning.service import ExecutionPlanner
from app.responsibilities.models import Responsibility, ResponsibilityPriority
from app.services.time_service import TimeService

class MockResponsibilityService:
    def __init__(self):
        self._responsibilities = []

    def add(self, r: Responsibility):
        self._responsibilities.append(r)

    def get_all(self):
        return self._responsibilities

def main():
    service = MockResponsibilityService()
    now = TimeService.now()
    today = now.replace(hour=23, minute=59, second=59)
    tomorrow = today + timedelta(days=1)
    yesterday = now - timedelta(days=1)

    r1 = Responsibility(title="High Tomorrow", priority=ResponsibilityPriority.HIGH, due_date=tomorrow)
    r2 = Responsibility(title="Critical Today", priority=ResponsibilityPriority.CRITICAL, due_date=today)
    r3 = Responsibility(title="Low Overdue", priority=ResponsibilityPriority.LOW, due_date=yesterday)
    r4 = Responsibility(title="Medium Today", priority=ResponsibilityPriority.MEDIUM, due_date=today)

    service.add(r1)
    service.add(r2)
    service.add(r3)
    service.add(r4)

    planner = ExecutionPlanner(service)
    plan = planner.generate_plan()

    for idx, r in enumerate(plan.responsibilities, 1):
        if r.due_date and r.due_date < now:
            status = "Overdue"
        elif r.due_date == today:
            status = "Today"
        else:
            status = "Tomorrow"
        print(f"{idx}. {r.title} [{r.priority.name}] ({status})")

if __name__ == "__main__":
    main()