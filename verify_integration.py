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
from app.services.briefing_formatter import BriefingFormatter

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
    
    # Scenario A: Only schedule.
    print("\n--- Scenario A: Only Schedule ---")
    cleanup(resp_service, event_service)
    schedule_context = "Today's Schedule\n- Quick Task"
    
    prompt = BriefingFormatter.build(schedule_context, "", "")
    print("Prompt Output:")
    print(repr(prompt))
    
    # Scenario B: Schedule + Memory
    print("\n--- Scenario B: Schedule + Memory ---")
    memory_context = "Relevant User Memories\n- I prefer coding at night."
    
    prompt = BriefingFormatter.build(schedule_context, memory_context, "")
    print("Prompt Output:")
    print(repr(prompt))
    
    # Scenario C: Schedule + Memory + Insights
    print("\n--- Scenario C: Schedule + Memory + Insights ---")
    insight_context = "Current Insights\n- [HIGH] Overloaded Day\n  You are overloaded."
    
    prompt = BriefingFormatter.build(schedule_context, memory_context, insight_context)
    print("Prompt Output:")
    print(repr(prompt))

if __name__ == "__main__":
    main()
