import re
from dataclasses import dataclass
from app.memory.models import Memory
from app.memory.service import MemoryService

@dataclass(frozen=True, slots=True)
class RelevantMemory:
    """A value object representing the retrieval result for a specific request."""
    query: str
    memories: list[Memory]

class MemoryRetriever:
    """
    Retrieves memories based on explicit, deterministic rules.
    Currently uses simple whitespace-tokenized keyword intersection.
    """
    
    def __init__(self, memory_service: MemoryService):
        self._service = memory_service
        
    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(re.findall(r"\w+", text.lower()))
        
    def retrieve(self, query: str) -> RelevantMemory:
        all_memories = self._service.get_all()
        
        query_tokens = self._tokenize(query)
        
        relevant_memories = []
        for memory in all_memories:
            memory_tokens = self._tokenize(memory.content)
            
            # Intersection check: any query token in memory OR any memory token in query
            if query_tokens.intersection(memory_tokens):
                relevant_memories.append(memory)
                
        # Return preserving creation order (get_all returns in order by default, and we just filter)
        return RelevantMemory(
            query=query,
            memories=relevant_memories
        )
