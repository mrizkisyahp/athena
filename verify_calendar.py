import sys
from datetime import datetime, timedelta
from app.calendar import EventService

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    service = EventService()
    
    print("--- Testing Event Creation ---")
    now = datetime.now()
    today = now.date()
    tomorrow = today + timedelta(days=1)
    
    e1 = service.create("Morning Meeting", now, now + timedelta(hours=1))
    e2 = service.create("Lunch", now + timedelta(hours=2), now + timedelta(hours=3))
    e3 = service.create("Thesis Work", now + timedelta(hours=4), now + timedelta(hours=6))
    
    # Tomorrow's meeting
    e4_start = datetime.combine(tomorrow, now.time())
    e4 = service.create("Tomorrow's Meeting", e4_start, e4_start + timedelta(hours=1))
    
    print("✓ Created 4 events")
    
    print("\n--- Testing Retrieval ---")
    all_events = service.get_all()
    if len(all_events) == 4:
        print("✓ get_all() returned 4 events")
    else:
        print(f"✗ get_all() returned {len(all_events)}")
        
    today_events = service.get_events_for_day(today)
    if len(today_events) == 3:
        print("✓ get_events_for_day(today) returned 3 events")
    else:
        print(f"✗ get_events_for_day(today) returned {len(today_events)}")
        
    fetched = service.get_by_id(e1.id)
    if fetched and fetched.title == "Morning Meeting":
        print("✓ get_by_id() returned correct event")
    else:
        print("✗ get_by_id() failed")
        
    not_found = service.get_by_id("invalid-id")
    if not_found is None:
        print("✓ get_by_id() for unknown ID returned None")
    else:
        print("✗ get_by_id() for unknown ID failed")
        
    print("\n--- Testing Deletion ---")
    deleted = service.delete(e1.id)
    if deleted:
        print("✓ delete() returned True for existing event")
    else:
        print("✗ delete() failed for existing event")
        
    unknown_delete = service.delete("invalid-id")
    if not unknown_delete:
        print("✓ delete() returned False for unknown ID")
    else:
        print("✗ delete() failed for unknown ID")
        
    if len(service.get_all()) == 3:
        print("✓ Remaining events: 3")
    else:
        print(f"✗ Remaining events: {len(service.get_all())}")

if __name__ == "__main__":
    main()
