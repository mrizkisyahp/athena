import sys
from datetime import datetime, timedelta
from app.calendar import Event

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("Creating valid event...")
    now = datetime.now()
    try:
        valid_event = Event(
            title="Team Sync",
            start_time=now,
            end_time=now + timedelta(hours=1),
            location="Room A",
            notes="Weekly sync"
        )
        print("✓ Success")
    except Exception as e:
        print(f"✗ Failed: {e}")
        
    print("\nCreating invalid event...")
    try:
        invalid_event = Event(
            title="Time Travel",
            start_time=now,
            end_time=now - timedelta(hours=1)
        )
        print("✗ Failed: Event creation should have raised ValueError")
    except ValueError as e:
        print(f"✓ Expected ValueError raised: {e}")
    except Exception as e:
        print(f"✗ Failed with unexpected exception: {e}")

if __name__ == "__main__":
    main()
