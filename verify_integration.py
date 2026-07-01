import sys
from datetime import datetime, date, time
from app.time.duration import Duration
from app.responsibilities.models import Responsibility, ResponsibilityPriority, ResponsibilityStatus
from app.responsibilities.service import ResponsibilityService
from app.calendar import EventService
from app.calendar.availability import AvailabilityEngine
from app.planning.service import ExecutionPlanner
from app.workload.service import WorkloadBalancer
from app.awareness.service import InsightEngine
from app.services.time_service import TimeService
from app.awareness.prompt import InsightPromptBuilder

def cleanup(resp_service, event_service):
    for r in resp_service.get_all():
        if r.status != ResponsibilityStatus.COMPLETED:
            resp_service.complete(r.id)
    for e in event_service.get_all():
        event_service.delete(e.id)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    resp_service = ResponsibilityService()
    event_service = EventService()
    availability = AvailabilityEngine(event_service)
    planner = ExecutionPlanner(resp_service, availability)
    workload = WorkloadBalancer(planner)
    engine = InsightEngine(planner, workload, availability)
    
    today = TimeService.now().date()
    capacity = Duration(minutes=480)
    
    # Scenario A: No insights.
    print("\n--- Scenario A: No Insights ---")
    cleanup(resp_service, event_service)
    # Add an event to eliminate large focus block (Rule 3)
    event_service.create("Block 1", datetime.combine(today, time(8,0)), datetime.combine(today, time(10,0)))
    event_service.create("Block 2", datetime.combine(today, time(11,0)), datetime.combine(today, time(13,0)))
    event_service.create("Block 3", datetime.combine(today, time(14,0)), datetime.combine(today, time(16,0)))
    event_service.create("Block 4", datetime.combine(today, time(17,0)), datetime.combine(today, time(19,0)))
    # Max free block is 1 hour
    
    # Add a task so schedule isn't empty (Rule 2) and is schedulable (Rule 4), and workload < capacity (Rule 1)
    resp_service.create("Quick Task", estimated_duration=Duration(minutes=30))
    
    insights = engine.generate(today, available_capacity=capacity)
    prompt = InsightPromptBuilder.build(insights)
    print(f"Insights length: {len(insights)}")
    print("Prompt Output:")
    print(repr(prompt))
    
    # Scenario B: Overloaded day.
    print("\n--- Scenario B: Overloaded Day ---")
    cleanup(resp_service, event_service)
    resp_service.create("Huge Task", priority=ResponsibilityPriority.HIGH, estimated_duration=Duration(minutes=540)) # 9 hours
    insights = engine.generate(today, available_capacity=capacity)
    prompt = InsightPromptBuilder.build(insights)
    print("Prompt Output:")
    print(prompt)
    
    # Scenario C: Multiple insights.
    print("\n--- Scenario C: Multiple Insights ---")
    cleanup(resp_service, event_service)
    event_service.create("Block Morning", datetime.combine(today, time(8,0)), datetime.combine(today, time(17,0)))
    resp_service.create("Huge Task", priority=ResponsibilityPriority.HIGH, estimated_duration=Duration(minutes=240)) # 4 hours
    
    insights = engine.generate(today, available_capacity=Duration(minutes=60))
    prompt = InsightPromptBuilder.build(insights)
    print("Prompt Output:")
    print(prompt)

if __name__ == "__main__":
    main()
