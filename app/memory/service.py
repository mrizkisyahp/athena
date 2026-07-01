from app.memory.models import Memory, MemoryType, MemoryImportance

class MemoryService:
    """
    Domain service responsible for managing Athena's long-term memories.
    Currently utilizes purely in-memory storage.
    """
    
    def __init__(self):
        self._memories: list[Memory] = []
        
    def create(self, memory_type: MemoryType, content: str, importance: MemoryImportance) -> Memory:
        """Creates and stores a new memory."""
        memory = Memory(
            memory_type=memory_type,
            content=content,
            importance=importance
        )
        self._memories.append(memory)
        return memory
        
    def get_all(self) -> list[Memory]:
        """Returns every stored memory."""
        # Return a copy to prevent external mutation of the internal list
        return list(self._memories)
        
    def get_by_id(self, memory_id: str) -> Memory | None:
        """Returns a specific memory by ID."""
        for memory in self._memories:
            if memory.id == memory_id:
                return memory
        return None
        
    def delete(self, memory_id: str) -> bool:
        """
        Deletes a memory by ID.
        Returns True if deleted, False if not found.
        """
        for i, memory in enumerate(self._memories):
            if memory.id == memory_id:
                del self._memories[i]
                return True
        return False
        
    def get_by_type(self, memory_type: MemoryType) -> list[Memory]:
        """Returns memories matching the requested category."""
        return [m for m in self._memories if m.memory_type == memory_type]
