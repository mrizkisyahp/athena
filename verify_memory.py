import sys
from app.memory import MemoryService, MemoryRetriever, MemoryType, MemoryImportance

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    service = MemoryService()
    
    # Clean up DB for clean test output
    for m in service.get_all():
        service.delete(m.id)
        
    print("--- Seeding Memories ---")
    service.create(MemoryType.PREFERENCE, "I prefer coding after dinner.", MemoryImportance.MEDIUM)
    service.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
    service.create(MemoryType.ROUTINE, "Review tasks every morning.", MemoryImportance.LOW)
    service.create(MemoryType.CONTEXT, "Working on Athena backend.", MemoryImportance.MEDIUM)
    print("✓ Seeded 4 memories")
    
    retriever = MemoryRetriever(service)
    
    queries = [
        "coding tonight",
        "graduate thesis",
        "backend sprint",
        "vacation beach"
    ]
    
    print("\n--- Running Retrieval Scenarios ---")
    for query in queries:
        print(f"Query:\n{query}\n↓\nReturns:")
        
        relevant = retriever.retrieve(query)
        if not relevant.memories:
            print("[]")
        else:
            for m in relevant.memories:
                print(f"{m.memory_type.name.capitalize()}: {m.content}")
        print()

if __name__ == "__main__":
    main()
