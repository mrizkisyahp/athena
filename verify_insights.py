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
    
    # Scenario 1: Overloaded day (High)
    print("\n--- Scenario 1: Overloaded Day ---")
    cleanup(resp_service, event_service)
    # Give a task that exceeds capacity
    resp_service.create("Huge Task", priority=ResponsibilityPriority.HIGH, estimated_duration=Duration(minutes=600))
    # Available capacity is let's say 8 hours
    insights = engine.generate(today, available_capacity=Duration(minutes=480))
    for i in insights:
        print(f"[{i.severity.value.upper()}] {i.title}: {i.description}")
        
    # Scenario 2: Empty schedule (Medium)
    print("\n--- Scenario 2: Empty Schedule ---")
    cleanup(resp_service, event_service)
    insights = engine.generate(today, available_capacity=Duration(minutes=480))
    for i in insights:
        print(f"[{i.severity.value.upper()}] {i.title}: {i.description}")
        
    # Scenario 3: Three-hour free block (Low)
    print("\n--- Scenario 3: Three-Hour Free Block ---")
    cleanup(resp_service, event_service)
    # Add a task so schedule isn't empty, but block remains large
    # 08:00 - 20:00 is default capacity. 12 hours.
    # Add an event from 12:00 to 13:00 to split it into 08:00-12:00 (4h) and 13:00-20:00 (7h)
    event_service.create("Lunch", datetime.combine(today, time(12,0)), datetime.combine(today, time(13,0)))
    resp_service.create("Quick Task", estimated_duration=Duration(minutes=30))
    # Schedule uses 08:00-08:30. Block 08:30-12:00 is 3.5 hrs.
    insights = engine.generate(today, available_capacity=Duration(minutes=480))
    for i in insights:
        print(f"[{i.severity.value.upper()}] {i.title}: {i.description}")
        
    # Scenario 4: Unknown-duration task (High)
    print("\n--- Scenario 4: Unscheduled Task ---")
    cleanup(resp_service, event_service)
    resp_service.create("Unknown Task") # No duration
    insights = engine.generate(today, available_capacity=Duration(minutes=480))
    for i in insights:
        print(f"[{i.severity.value.upper()}] {i.title}: {i.description}")
        
    # Scenario 5: Multiple conditions
    print("\n--- Scenario 5: Multiple Conditions ---")
    cleanup(resp_service, event_service)
    # Give a task that takes 4 hours, but availability is 1 hour.
    # The actual free block is 3 hours, so it doesn't fit (unscheduled, empty schedule).
    # Since 3 hours >= 2 hours, it triggers Idle Capacity (Low).
    event_service.create("Block Morning", datetime.combine(today, time(8,0)), datetime.combine(today, time(17,0)))
    # Free block is 17:00 to 20:00 (3 hours).
    
    resp_service.create("Huge Task", priority=ResponsibilityPriority.HIGH, estimated_duration=Duration(minutes=240)) # 4 hours
    insights = engine.generate(today, available_capacity=Duration(minutes=60)) # 1 hour capacity
    for i in insights:
        print(f"[{i.severity.value.upper()}] {i.title}: {i.description}")

if __name__ == "__main__":
    main()
