from app.planning.service import ExecutionPlanner
from app.responsibilities.models import Responsibility
from app.time.duration import Duration
from app.services.time_service import TimeService

class MockResponsibilityService:
    def __init__(self):
        self._responsibilities = []

    def add(self, r: Responsibility):
        self._responsibilities.append(r)

    def get_all(self):
        return self._responsibilities

def run_scenario(scenario_name: str, durations: list[int | None]):
    service = MockResponsibilityService()
    
    for i, d in enumerate(durations):
        r = Responsibility(title=f"Task {i}")
        if d is not None:
            r.estimated_duration = Duration(d)
        service.add(r)
        
    planner = ExecutionPlanner(service)
    plan = planner.generate_plan()
    
    print(f"--- {scenario_name} ---")
    if plan.total_estimated_duration:
        print(f"Total: {plan.total_estimated_duration}")
    else:
        print("Total: Unknown")
    print()

def main():
    run_scenario("Scenario 1", [90, 120, 60])
    run_scenario("Scenario 2", [90, None, 60])
    run_scenario("Scenario 3", [None, None])

if __name__ == "__main__":
    main()