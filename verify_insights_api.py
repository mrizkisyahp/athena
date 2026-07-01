import sys
import json
from datetime import datetime, time
from fastapi.testclient import TestClient

from app.main import app
from app.bootstrap.container import container
from app.time.duration import Duration
from app.responsibilities.models import ResponsibilityPriority, ResponsibilityStatus
from app.services.time_service import TimeService

def cleanup():
    for r in container.responsibilities.get_all():
        if r.status != ResponsibilityStatus.COMPLETED:
            container.responsibilities.complete(r.id)
    for e in container.events.get_all():
        container.events.delete(e.id)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    client = TestClient(app)
    today = TimeService.now().date()
    
    cleanup()
    
    # We want to match exactly what the TL expects: Overloaded Day & Unscheduled Responsibilities.
    # To get Unscheduled Responsibilities (HIGH), we need a task that doesn't fit in any block.
    # And we also want Overloaded Day (HIGH), which means total workload > capacity.
    # capacity is BRIEFING_INSIGHT_CAPACITY (8 hours = 480 mins).
    # We can create a 9 hour task. It will be > 8 hours (Overloaded) and > max free block (Unscheduled, since max free is 24 hours but wait...)
    # Wait, if we don't have events, the max free block is 24 hours. A 9 hour task CAN be scheduled.
    # So we need to create events so that the max free block is < 9 hours.
    # Let's add an event that blocks the middle of the day.
    
    container.events.create(
        "Middle Block",
        datetime.combine(today, time(12, 0)),
        datetime.combine(today, time(13, 0))
    )
    # 00:00 to 12:00 = 12 hours.
    # 13:00 to 24:00 = 11 hours.
    # So a 13-hour task won't fit in any free block!
    # And 13 hours > 8 hours, so it's Overloaded.
    
    container.responsibilities.create(
        title="Huge Task",
        priority=ResponsibilityPriority.HIGH,
        estimated_duration=Duration(minutes=13 * 60)
    )
    
    # Call the API
    response = client.get("/insights")
    
    assert response.status_code == 200
    data = response.json()
    
    # We expect 2 insights. Wait, "Large Focus Block Available" might trigger if there's a 12 hour block.
    # To prevent that, let's just accept 3 insights and print them, or filter the print to only title and severity.
    
    print(json.dumps([
        {
            "title": i["title"],
            "severity": i["severity"]
        } for i in data
    ], indent=2))
    
    cleanup()

if __name__ == "__main__":
    main()
