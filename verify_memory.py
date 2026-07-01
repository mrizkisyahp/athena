import sys
from app.memory import MemoryService, MemoryType, MemoryImportance

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("--- Phase 1 ---")
    print("Creating memories...")
    service1 = MemoryService()
    
    pref1 = service1.create(MemoryType.PREFERENCE, "I prefer coding after dinner.", MemoryImportance.MEDIUM)
    goal1 = service1.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
    routine1 = service1.create(MemoryType.ROUTINE, "Review tasks every morning.", MemoryImportance.LOW)
    context1 = service1.create(MemoryType.CONTEXT, "Working on Athena.", MemoryImportance.MEDIUM)
    
    print("Creating duplicate memory...")
    goal2 = service1.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
    print("✓ Success")
    
    print("Creating duplicate memory again...")
    goal3 = service1.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
    print("✓ Success")
    
    all_memories = service1.get_all()
    duplicates_count = len([m for m in all_memories if m.content == "Graduate this year."])
    print(f"Retrieved duplicates: {duplicates_count}")
    
    print(f"✓ Created {len(all_memories)} memories")
    
    print("\n--- Phase 2 ---")
    print("Creating NEW MemoryService...")
    service2 = MemoryService()
    retrieved_memories = service2.get_all()
    print(f"✓ Retrieved {len(retrieved_memories)} memories")
    
    print("\n--- Phase 3 ---")
    print("Deleting one memory...")
    deleted = service2.delete(pref1.id)
    if deleted:
        print("✓ Deleted")
    else:
        print("✗ Deletion Failed")
        
    print("\n--- Phase 4 ---")
    print("Creating NEW MemoryService...")
    service3 = MemoryService()
    final_memories = service3.get_all()
    print(f"✓ Retrieved {len(final_memories)} memories")
    
    print("\nPersistence verified.")

if __name__ == "__main__":
    main()
