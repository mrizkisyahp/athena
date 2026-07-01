from app.memory.retrieval import RelevantMemory

class MemoryPromptBuilder:
    """Formats retrieved memories into a consistent prompt context block."""
    
    @staticmethod
    def build(relevant: RelevantMemory) -> str:
        if not relevant.memories:
            return ""
            
        memories_list = "\n".join(f"- {m.content}" for m in relevant.memories)
        return f"\nRelevant User Memories\n\n{memories_list}\n"
