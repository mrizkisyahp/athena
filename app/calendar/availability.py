from dataclasses import dataclass
from datetime import datetime, date, time
from app.calendar.models import Event
from app.calendar.service import EventService
from app.time.duration import Duration


@dataclass(frozen=True, slots=True)
class TimeBlock:
    start: datetime
    end: datetime

    @property
    def duration(self) -> Duration:
        delta = self.end - self.start
        return Duration(minutes=int(delta.total_seconds() // 60))


@dataclass(frozen=True, slots=True)
class DailyAvailability:
    date: date
    occupied: list[Event]
    free_blocks: list[TimeBlock]


class AvailabilityEngine:
    """
    Computes free time blocks based on calendar events.
    """
    def __init__(self, event_service: EventService):
        self._events = event_service

    def calculate(self, day: date) -> DailyAvailability:
        # Hardcoded working hours for V1
        work_start = datetime.combine(day, time(hour=8, minute=0))
        work_end = datetime.combine(day, time(hour=20, minute=0))

        events = self._events.get_events_for_day(day)
        
        # Sort chronologically by start time
        sorted_events = sorted(events, key=lambda e: e.start_time)
        
        occupied = []
        free_blocks = []
        
        current_time = work_start
        
        for event in sorted_events:
            # We only care about events that overlap with working hours
            if event.end_time <= work_start or event.start_time >= work_end:
                continue
                
            # Cap the event bounds strictly to the working day
            eff_start = max(event.start_time, work_start)
            eff_end = min(event.end_time, work_end)
            
            occupied.append(event)
            
            # Is there a free gap before this event?
            if eff_start > current_time:
                gap = eff_start - current_time
                if gap.total_seconds() > 0:
                    free_blocks.append(TimeBlock(start=current_time, end=eff_start))
                    
            # Move the pointer to the end of this event
            current_time = max(current_time, eff_end)
            
        # Add any remaining free block after the last event
        if current_time < work_end:
            gap = work_end - current_time
            if gap.total_seconds() > 0:
                free_blocks.append(TimeBlock(start=current_time, end=work_end))
                
        return DailyAvailability(
            date=day,
            occupied=occupied,
            free_blocks=free_blocks
        )
