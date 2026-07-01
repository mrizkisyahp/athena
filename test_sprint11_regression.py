import sys
from datetime import datetime, date, time, timedelta

from app.time.duration import Duration
from app.responsibilities.models import Responsibility, ResponsibilityPriority, ResponsibilityStatus
from app.responsibilities.service import ResponsibilityService
from app.calendar import Event, EventService
from app.calendar.availability import AvailabilityEngine
from app.planning.service import ExecutionPlanner
from app.services.time_service import TimeService
from app.database.session import engine
from sqlalchemy import text

def test_event_domain():
    now = TimeService.now()
    e = Event(title="Test", start_time=now, end_time=now + timedelta(hours=1))
    assert e.title == "Test"
    # test immutability
    try:
        e.title = "Changed"
        return False
    except AttributeError:
        pass
    return True

def test_event_persistence():
    service = EventService()
    now = TimeService.now()
    today = now.date()
    
    e1 = service.create("Morning Meeting", now, now + timedelta(hours=1))
    service2 = EventService()
    fetched = service2.get_by_id(e1.id)
    if not fetched:
        return False
        
    all_events = service2.get_all()
    if not any(e.id == e1.id for e in all_events):
        return False
        
    day_events = service2.get_events_for_day(today)
    if not any(e.id == e1.id for e in day_events):
        return False
        
    service2.delete(e1.id)
    if service2.get_by_id(e1.id):
        return False
        
    return True

def test_availability_engine():
    event_service = EventService()
    today = TimeService.now().date()
    
    # Clean up for clean test
    for e in event_service.get_events_for_day(today):
        event_service.delete(e.id)
        
    event_service.create("Meeting", datetime.combine(today, time(9, 0)), datetime.combine(today, time(10, 0)))
    event_service.create("Lunch", datetime.combine(today, time(12, 0)), datetime.combine(today, time(13, 0)))
    
    av_engine = AvailabilityEngine(event_service)
    av = av_engine.calculate(today)
    
    # 08:00-09:00, 10:00-12:00, 13:00-20:00 = 3 free blocks
    if len(av.free_blocks) != 3:
        return False
        
    b1 = av.free_blocks[0]
    if b1.start.time() != time(8, 0) or b1.end.time() != time(9, 0):
        return False
        
    # Duration of b1 is 60 minutes
    if b1.duration.minutes != 60:
        return False
        
    # Zero gap test
    event_service.create("Consecutive", datetime.combine(today, time(10, 0)), datetime.combine(today, time(12, 0)))
    av2 = av_engine.calculate(today)
    if len(av2.free_blocks) != 2: # 08:00-09:00, 13:00-20:00
        return False
        
    for e in event_service.get_events_for_day(today):
        event_service.delete(e.id)
        
    return True
    
def test_calendar_scheduling():
    resp_service = ResponsibilityService()
    event_service = EventService()
    
    for r in resp_service.get_all():
        if r.status != ResponsibilityStatus.COMPLETED:
            resp_service.complete(r.id)
            
    for e in event_service.get_all():
        event_service.delete(e.id)
        
    today = TimeService.now().date()
    event_service.create("Morning", datetime.combine(today, time(9, 0)), datetime.combine(today, time(10, 0)))
    
    resp_service.create("Task1", priority=ResponsibilityPriority.HIGH, estimated_duration=Duration(minutes=30))
    resp_service.create("Task2", priority=ResponsibilityPriority.LOW) # Unknown
    
    av_engine = AvailabilityEngine(event_service)
    planner = ExecutionPlanner(resp_service, av_engine)
    
    schedule = planner.generate_schedule(today)
    
    # Task1 is 30 mins, free block starts 08:00, so it schedules at 08:00
    if len(schedule.tasks) != 1:
        return False
        
    if schedule.tasks[0].start_time.time() != time(8, 0):
        return False
        
    if len(schedule.unscheduled) != 1 or schedule.unscheduled[0].title != "Task2":
        return False
        
    # Cleanup
    for r in resp_service.get_all():
        if r.status != ResponsibilityStatus.COMPLETED:
            resp_service.complete(r.id)
    for e in event_service.get_all():
        event_service.delete(e.id)
        
    return True
    
def test_existing_systems():
    # Simply test that executing the planner doesn't fail
    resp_service = ResponsibilityService()
    planner = ExecutionPlanner(resp_service, None)
    plan = planner.generate_plan()
    if not hasattr(plan, 'responsibilities'):
        return False
    return True
    
def test_database_integrity():
    try:
        with engine.connect() as conn:
            # Test schema exists
            conn.execute(text("SELECT id FROM events LIMIT 1"))
            conn.execute(text("SELECT id FROM memories LIMIT 1"))
            conn.execute(text("SELECT id FROM responsibilities LIMIT 1"))
            conn.execute(text("SELECT id FROM projects LIMIT 1"))
            return True
    except Exception as e:
        print(e)
        return False

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("--- Running Sprint 11 Regression Suite ---\n")
    
    tests = [
        ("1. Testing Event Domain", test_event_domain),
        ("2. Testing Event Persistence", test_event_persistence),
        ("3. Testing Availability Engine", test_availability_engine),
        ("4. Testing Calendar Scheduling", test_calendar_scheduling),
        ("5. Testing Existing Systems", test_existing_systems),
        ("6. Testing Database Integrity", test_database_integrity),
    ]
    
    all_passed = True
    for name, test_fn in tests:
        # Pad with dots
        padded_name = name + "." * (40 - len(name))
        
        try:
            if test_fn():
                print(f"{padded_name}[PASS]")
            else:
                print(f"{padded_name}[FAIL]")
                all_passed = False
        except Exception as e:
            print(f"{padded_name}[FAIL (Exception: {e})]")
            all_passed = False
            
    if all_passed:
        print("\nALL TESTS PASSED!\n")
        print("Sprint 11 regression testing successful.")
    else:
        print("\nSOME TESTS FAILED.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
