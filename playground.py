from app.advisors.capacity import CapacityAdvisor
from app.planning.service import ExecutionPlanner
from app.responsibilities.models import Responsibility
from app.time.duration import Duration

class MockResponsibilityService:
    def __init__(self):
        self._responsibilities = []

    def add(self, r: Responsibility):
        self._responsibilities.append(r)

    def get_all(self):
        return self._responsibilities

def run_scenario(scenario_name: str, plan_duration: int | None, cap_str: str):
    service = MockResponsibilityService()
    
    if plan_duration is not None:
        r = Responsibility(title="Task 1", estimated_duration=Duration(plan_duration))
        service.add(r)
    else:
        r = Responsibility(title="Task 1", estimated_duration=None)
        service.add(r)

    planner = ExecutionPlanner(service)
    advisor = CapacityAdvisor(planner)
    
    decision = advisor.advise(cap_str)
    
    print(f"--- {scenario_name} ---")
    print(f"Decision: {decision.outcome.value}")
    print(f"Reason: {decision.reasoning[0] if decision.reasoning else 'No reason'}\n")

def main():
    run_scenario("Scenario 1 (Plan 4 hr, Cap 5 hr)", 240, "I have 5 hours")
    run_scenario("Scenario 2 (Plan 4 hr, Cap 2 hr)", 240, "I have 2 hours")
    run_scenario("Scenario 3 (Plan Unknown)", None, "I have 5 hours")

if __name__ == "__main__":
    main()