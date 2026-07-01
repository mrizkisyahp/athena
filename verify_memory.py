from app.memory import Memory, MemoryType, MemoryImportance

def main():
    pref_mem = Memory(
        memory_type=MemoryType.PREFERENCE,
        content="I prefer coding after dinner.",
        importance=MemoryImportance.MEDIUM
    )

    goal_mem = Memory(
        memory_type=MemoryType.GOAL,
        content="Graduate this year.",
        importance=MemoryImportance.HIGH
    )

    routine_mem = Memory(
        memory_type=MemoryType.ROUTINE,
        content="Review tasks every morning.",
        importance=MemoryImportance.LOW
    )
    
    print("Constructed Memories:")
    print(pref_mem)
    print(goal_mem)
    print(routine_mem)

if __name__ == "__main__":
    main()
