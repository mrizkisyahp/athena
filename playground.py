import asyncio
from app.planning.service import ExecutionPlanner
from app.responsibilities.models import Responsibility, ResponsibilityPriority
from app.services.time_service import TimeService
from app.time.duration import Duration
from app.workload.service import WorkloadBalancer
from app.workload.workload_service import WorkloadService
from app.bootstrap.container import container

class MockResponsibilityService:
    def __init__(self):
        self._responsibilities = []

    def add(self, r: Responsibility):
        self._responsibilities.append(r)

    def get_all(self):
        return self._responsibilities

def run_scenario(scenario_name: str, cap_hr: float, tasks: list[Responsibility]):
    service = MockResponsibilityService()
    for t in tasks:
        service.add(t)

    planner = ExecutionPlanner(service)
    balancer = WorkloadBalancer(planner)
    
    analysis = balancer.analyze(Duration(int(cap_hr * 60)))
    
    print(f"--- {scenario_name} ---")
    print(f"Overloaded: {analysis.overloaded}")
    print(f"Deferrals: {[t.title for t in analysis.suggested_deferrals]}")
    print(f"Reasoning: {analysis.reasoning[-1] if analysis.reasoning else ''}\n")

def main():
    now = TimeService.now()
    
    t1 = Responsibility(title="Sprint 9", project_id="Athena", estimated_duration=Duration(90), priority=ResponsibilityPriority.HIGH)
    t2 = Responsibility(title="Athena", project_id="Athena", estimated_duration=Duration(60), priority=ResponsibilityPriority.HIGH)
    t3 = Responsibility(title="Thesis", project_id="Thesis", estimated_duration=Duration(90), priority=ResponsibilityPriority.HIGH)
    
    run_scenario(
        "Scenario 1 (Cap: 150m, Plan: 240m)",
        2.5, # 150 minutes
        [t1, t2, t3]
    )
    
    t4 = Responsibility(title="Sprint 9", project_id="Athena", estimated_duration=Duration(60), priority=ResponsibilityPriority.HIGH)
    t5 = Responsibility(title="Fix API", project_id="Athena", estimated_duration=Duration(60), priority=ResponsibilityPriority.HIGH)
    t6 = Responsibility(title="Write Docs", project_id="Athena", estimated_duration=Duration(60), priority=ResponsibilityPriority.HIGH)
    
    run_scenario(
        "Scenario 2 (Cap: 60m, Plan: 180m)",
        1, # 60 minutes
        [t4, t5, t6]
    )
    
    t7_crit = Responsibility(title="Critical Today", project_id="Athena", estimated_duration=Duration(120), priority=ResponsibilityPriority.CRITICAL, due_date=now)
    t8_crit = Responsibility(title="Personal", project_id="Personal", estimated_duration=Duration(120), priority=ResponsibilityPriority.CRITICAL, due_date=now)
    
    run_scenario(
        "Scenario 3 (All protected)",
        2,
        [t7_crit, t8_crit]
    )

if __name__ == "__main__":
    main()