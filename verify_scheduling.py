import sys
from datetime import datetime, date, time, timedelta
from app.time.duration import Duration
from app.responsibilities.models import Responsibility, ResponsibilityPriority, ResponsibilityStatus
from app.responsibilities.service import ResponsibilityService
from app.calendar import EventService
from app.calendar.availability import AvailabilityEngine
from app.planning.service import ExecutionPlanner
from app.services.time_service import TimeService

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Reset singletons/data if any, or just use fresh services
    resp_service = ResponsibilityService()
    event_service = EventService()
    
    # Cleanup previous run (if any)
    for r in resp_service.get_all():
        resp_service.complete(r.id)
    for e in event_service.get_all():
        event_service.delete(e.id)
        
    engine = AvailabilityEngine(event_service)
    planner = ExecutionPlanner(resp_service, engine)
    
    now = TimeService.now()
    today = now.date()
    
    # Seed events
    event_service.create("Meeting", datetime.combine(today, time(9, 0)), datetime.combine(today, time(10, 0)))
    event_service.create("Lunch", datetime.combine(today, time(12, 0)), datetime.combine(today, time(13, 0)))
    
    # Seed tasks
    resp_service.create("Fix API", priority=ResponsibilityPriority.HIGH, estimated_duration=Duration(minutes=45))
    resp_service.create("Thesis", priority=ResponsibilityPriority.MEDIUM, estimated_duration=Duration(minutes=90))
    resp_service.create("Buy Milk", priority=ResponsibilityPriority.LOW, estimated_duration=Duration(minutes=20))
    resp_service.create("Research", priority=ResponsibilityPriority.LOW) # Unknown
    
    schedule = planner.generate_schedule(today)
    
    print("Scheduled Tasks")
    for st in schedule.tasks:
        print(f"{st.start_time.strftime('%H:%M')}-{st.end_time.strftime('%H:%M')} {st.responsibility.title}")
        
    print("\n----------------\n")
    
    print("Unscheduled")
    for r in schedule.unscheduled:
        dur = f"{r.estimated_duration.minutes} min" if r.estimated_duration else "Unknown duration"
        print(f"{r.title} ({dur})")

if __name__ == "__main__":
    main()
