from app.memory import MemoryService, MemoryType, MemoryImportance

def main():
    service = MemoryService()
    
    print("--- 1. Testing Creation & Duplicates ---")
    pref1 = service.create(MemoryType.PREFERENCE, "I prefer coding after dinner.", MemoryImportance.MEDIUM)
    goal1 = service.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
    routine1 = service.create(MemoryType.ROUTINE, "Review tasks every morning.", MemoryImportance.LOW)
    context1 = service.create(MemoryType.CONTEXT, "Working on Athena.", MemoryImportance.MEDIUM)
    
    # Testing duplicate content
    goal2 = service.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
    
    print(f"Created {len(service.get_all())} memories.")
    print("Duplicates allowed:", goal1.content == goal2.content and goal1.id != goal2.id)

    print("\n--- 2. Testing Get By Type ---")
    goals = service.get_by_type(MemoryType.GOAL)
    print(f"Found {len(goals)} goals (should be 2).")
    for g in goals:
        print(f"  - {g.content} (ID: {g.id})")

    print("\n--- 3. Testing Get By ID ---")
    retrieved = service.get_by_id(pref1.id)
    print(f"Retrieved preference by ID: {retrieved is not None and retrieved.content == pref1.content}")
    
    unknown = service.get_by_id("fake-id")
    print(f"Unknown ID returns None: {unknown is None}")

    print("\n--- 4. Testing Deletion ---")
    deleted = service.delete(routine1.id)
    print(f"Successfully deleted routine memory: {deleted}")
    
    failed_delete = service.delete("fake-id")
    print(f"Failed deletion returns False: {failed_delete is False}")
    
    print("\n--- 5. Final State ---")
    final_memories = service.get_all()
    print(f"Memories remaining: {len(final_memories)} (should be 4)")

if __name__ == "__main__":
    main()
