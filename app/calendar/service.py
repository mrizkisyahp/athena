from datetime import datetime, date
from app.calendar.models import Event
from app.database.session import SessionLocal
from app.database.models import EventORM
import app.database.mappers as mappers

class EventService:
    """
    Domain service responsible for managing calendar events.
    Backed by PostgreSQL storage.
    """
    
    def create(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        location: str | None = None,
        notes: str | None = None,
    ) -> Event:
        """Creates and stores a new event in the database."""
        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            notes=notes
        )
        
        with SessionLocal() as session:
            orm_event = mappers.to_event_orm(event)
            session.add(orm_event)
            session.commit()
            
        return event
        
    def get_all(self) -> list[Event]:
        """Returns every stored event."""
        with SessionLocal() as session:
            orm_events = session.query(EventORM).order_by(EventORM.created_at).all()
            return [mappers.to_event_domain(orm) for orm in orm_events]
            
    def get_by_id(self, event_id: str) -> Event | None:
        """Returns a specific event by ID, or None if not found."""
        with SessionLocal() as session:
            orm_event = session.query(EventORM).filter(EventORM.id == event_id).first()
            if orm_event:
                return mappers.to_event_domain(orm_event)
            return None
            
    def delete(self, event_id: str) -> bool:
        """
        Deletes a specific event by ID.
        Returns True if deleted, False if not found.
        """
        with SessionLocal() as session:
            orm_event = session.query(EventORM).filter(EventORM.id == event_id).first()
            if not orm_event:
                return False
            session.delete(orm_event)
            session.commit()
            return True
            
    def get_events_for_day(self, day: date) -> list[Event]:
        """
        Returns events scheduled for a specific day, preserving creation order.
        Filters using start_time.date() == day.
        """
        return [e for e in self.get_all() if e.start_time.date() == day]
