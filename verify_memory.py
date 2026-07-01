import sys
import asyncio
from app.bootstrap.container import container
from app.memory import MemoryType, MemoryImportance

async def async_main():
    service = container.memories
    
    # Clean up DB for clean test output
    for m in service.get_all():
        service.delete(m.id)
        
    print("--- Seeding Memories ---")
    service.create(MemoryType.PREFERENCE, "I prefer coding after dinner.", MemoryImportance.MEDIUM)
    service.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
    print("✓ Seeded 2 memories")
    
    print("\n=================================")
    print("      WITH MEMORIES SEEDED")
    print("=================================\n")
    
    print("--- Daily Briefing ---")
    briefing = await container.briefing.generate_daily_briefing()
    print(briefing)
    
    print("\n--- Execution Plan ---")
    plan = await container.planning_service.generate_plan()
    print(plan)
    
    print("\n--- Advisor ---")
    advice = await container.advisor_service.advise("Can I game tonight?")
    print(advice)
    
    print("\n=================================")
    print("        MEMORIES CLEARED")
    print("=================================\n")
    for m in service.get_all():
        service.delete(m.id)
        
    print("--- Daily Briefing ---")
    briefing_no_mem = await container.briefing.generate_daily_briefing()
    print(briefing_no_mem)
    
    print("\n--- Execution Plan ---")
    plan_no_mem = await container.planning_service.generate_plan()
    print(plan_no_mem)
    
    print("\n--- Advisor ---")
    advice_no_mem = await container.advisor_service.advise("Can I game tonight?")
    print(advice_no_mem)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
