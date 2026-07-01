from sqlalchemy import select

from app.memory.models import Memory, MemoryType, MemoryImportance
from app.database.session import SessionLocal
from app.database.models import MemoryORM
import app.database.mappers as mappers

class MemoryService:
    """
    Domain service responsible for managing Athena's long-term memories.
    Utilizes PostgreSQL for persistence.
    """
    
    def __init__(self):
        self._session_factory = SessionLocal
        
    def create(self, memory_type: MemoryType, content: str, importance: MemoryImportance) -> Memory:
        """Creates and stores a new memory."""
        memory = Memory(
            memory_type=memory_type,
            content=content,
            importance=importance
        )
        orm_model = mappers.to_memory_orm(memory)

        with self._session_factory() as session:
            session.add(orm_model)
            session.commit()
            
        return memory
        
    def get_all(self) -> list[Memory]:
        """Returns every stored memory."""
        with self._session_factory() as session:
            models = session.scalars(select(MemoryORM)).all()
            return [mappers.to_memory_domain(model) for model in models]
        
    def get_by_id(self, memory_id: str) -> Memory | None:
        """Returns a specific memory by ID."""
        with self._session_factory() as session:
            model = session.get(MemoryORM, memory_id)
            if not model:
                return None
            return mappers.to_memory_domain(model)
        
    def delete(self, memory_id: str) -> bool:
        """
        Deletes a memory by ID.
        Returns True if deleted, False if not found.
        """
        with self._session_factory() as session:
            model = session.get(MemoryORM, memory_id)
            if not model:
                return False
            session.delete(model)
            session.commit()
            return True
        
    def get_by_type(self, memory_type: MemoryType) -> list[Memory]:
        """Returns memories matching the requested category."""
        with self._session_factory() as session:
            stmt = select(MemoryORM).where(MemoryORM.memory_type == memory_type.value)
            models = session.scalars(stmt).all()
            return [to_memory_domain(model) for model in models]
