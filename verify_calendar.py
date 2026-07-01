import sys
from datetime import datetime, timedelta
from app.calendar import EventService

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Cleanup previous run
    service = EventService()
    for e in service.get_all():
        service.delete(e.id)
        
    print("--- Phase 1 ---")
    now = datetime.now()
    today = now.date()
    tomorrow = today + timedelta(days=1)
    
    e1 = service.create("Morning Meeting", now, now + timedelta(hours=1))
    e2 = service.create("Lunch", now + timedelta(hours=2), now + timedelta(hours=3))
    e3 = service.create("Thesis Work", now + timedelta(hours=4), now + timedelta(hours=6))
    e4_start = datetime.combine(tomorrow, now.time())
    e4 = service.create("Tomorrow's Meeting", e4_start, e4_start + timedelta(hours=1))
    print("✓ Created 4 events")
    
    print("\n--- Phase 2 ---")
    service2 = EventService()
    all_events = service2.get_all()
    if len(all_events) == 4:
        print("✓ Retrieved 4 events")
    else:
        print(f"✗ Retrieved {len(all_events)} events")
        
    print("\n--- Phase 3 ---")
    deleted = service2.delete(e1.id)
    if deleted:
        print("✓ Deleted")
    else:
        print("✗ Deletion failed")
        
    print("\n--- Phase 4 ---")
    service3 = EventService()
    if len(service3.get_all()) == 3:
        print("✓ Retrieved 3 events")
    else:
        print(f"✗ Retrieved {len(service3.get_all())} events")
        
    print("\n--- Phase 5 ---")
    today_events = service3.get_events_for_day(today)
    if len(today_events) == 2: # 1 was deleted
        print("✓ get_events_for_day(today) returned exactly today's remaining events")
    else:
        print(f"✗ get_events_for_day(today) returned {len(today_events)}")

if __name__ == "__main__":
    main()
