import sys
from datetime import datetime, date, time, timedelta
from app.calendar import EventService
from app.calendar.availability import AvailabilityEngine

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Use real container or just instantiated services
    service = EventService()
    
    # Cleanup previous run (if any)
    for e in service.get_all():
        service.delete(e.id)
        
    engine = AvailabilityEngine(service)
    
    today = date.today()
    
    # Create the events as specified
    service.create("Meeting", datetime.combine(today, time(9, 0)), datetime.combine(today, time(10, 0)))
    service.create("Lunch", datetime.combine(today, time(12, 0)), datetime.combine(today, time(13, 0)))
    service.create("Thesis", datetime.combine(today, time(15, 0)), datetime.combine(today, time(17, 0)))
    
    availability = engine.calculate(today)
    
    print("Occupied")
    for event in availability.occupied:
        print(f"{event.start_time.strftime('%H:%M')}-{event.end_time.strftime('%H:%M')} {event.title}")
        
    print("\n------------------\n")
    
    print("Free Blocks")
    for block in availability.free_blocks:
        print(f"{block.start.strftime('%H:%M')}-{block.end.strftime('%H:%M')} ({block.duration})")

if __name__ == "__main__":
    main()
