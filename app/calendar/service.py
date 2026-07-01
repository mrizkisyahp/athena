from datetime import datetime, date
from app.calendar.models import Event

class EventService:
    """
    Domain service responsible for managing calendar events.
    Currently backed by in-memory storage.
    """
    
    def __init__(self):
        self._events: list[Event] = []
        
    def create(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        location: str | None = None,
        notes: str | None = None,
    ) -> Event:
        """Creates and stores a new event."""
        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            notes=notes
        )
        self._events.append(event)
        return event
        
    def get_all(self) -> list[Event]:
        """Returns every stored event. (Defensive copy)"""
        return list(self._events)
        
    def get_by_id(self, event_id: str) -> Event | None:
        """Returns a specific event by ID, or None if not found."""
        for event in self._events:
            if event.id == event_id:
                return event
        return None
        
    def delete(self, event_id: str) -> bool:
        """
        Deletes a specific event by ID.
        Returns True if deleted, False if not found.
        """
        for i, event in enumerate(self._events):
            if event.id == event_id:
                del self._events[i]
                return True
        return False
        
    def get_events_for_day(self, day: date) -> list[Event]:
        """
        Returns events scheduled for a specific day, preserving creation order.
        Filters using start_time.date() == day.
        """
        return [e for e in self._events if e.start_time.date() == day]
