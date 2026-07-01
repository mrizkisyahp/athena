from app.planning.service import ExecutionPlanner
from app.responsibilities.models import Responsibility, ResponsibilityPriority
from app.services.time_service import TimeService
from app.time.duration import Duration
from app.workload.service import WorkloadBalancer

class MockResponsibilityService:
    def __init__(self):
        self._responsibilities = []

    def add(self, r: Responsibility):
        self._responsibilities.append(r)

    def get_all(self):
        return self._responsibilities

def run_scenario(scenario_name: str, cap_hr: int, tasks: list[Responsibility]):
    service = MockResponsibilityService()
    for t in tasks:
        service.add(t)

    planner = ExecutionPlanner(service)
    balancer = WorkloadBalancer(planner)
    
    analysis = balancer.analyze(Duration(cap_hr * 60))
    
    print(f"--- {scenario_name} ---")
    print(f"Overloaded: {analysis.overloaded}")
    print(f"Deferrals: {[t.title for t in analysis.suggested_deferrals]}")
    print(f"Reasoning: {analysis.reasoning[0] if analysis.reasoning else ''}\n")

def main():
    now = TimeService.now()
    
    t1 = Responsibility(title="Sprint 9", estimated_duration=Duration(120), priority=ResponsibilityPriority.HIGH)
    t2 = Responsibility(title="Thesis Review", estimated_duration=Duration(120), priority=ResponsibilityPriority.HIGH)
    
    run_scenario(
        "Scenario 1 (Cap: 6 hr, Plan: 4 hr)",
        6,
        [t1, t2]
    )
    
    t3 = Responsibility(title="Buy Milk", estimated_duration=Duration(60), priority=ResponsibilityPriority.LOW)
    t4 = Responsibility(title="Clean Downloads", estimated_duration=Duration(60), priority=ResponsibilityPriority.LOW)
    
    run_scenario(
        "Scenario 2 (Cap: 4 hr, Plan: 6 hr)",
        4,
        [t1, t2, t3, t4]
    )
    
    t1_crit = Responsibility(title="Sprint 9", estimated_duration=Duration(120), priority=ResponsibilityPriority.CRITICAL, due_date=now)
    t2_crit = Responsibility(title="Thesis Review", estimated_duration=Duration(120), priority=ResponsibilityPriority.CRITICAL, due_date=now)
    t3_crit = Responsibility(title="Buy Milk", estimated_duration=Duration(60), priority=ResponsibilityPriority.CRITICAL, due_date=now)
    t4_crit = Responsibility(title="Clean Downloads", estimated_duration=Duration(60), priority=ResponsibilityPriority.CRITICAL, due_date=now)
    
    run_scenario(
        "Scenario 3 (All protected)",
        4,
        [t1_crit, t2_crit, t3_crit, t4_crit]
    )

if __name__ == "__main__":
    main()