import sys
import asyncio
from datetime import datetime
from dataclasses import FrozenInstanceError

from app.memory.models import Memory, MemoryType, MemoryImportance
from app.memory.service import MemoryService
from app.memory.retrieval import MemoryRetriever
from app.memory.prompt import MemoryPromptBuilder
from app.memory.constants import BRIEFING_QUERY, PLANNING_QUERY

from app.database.session import engine
from sqlalchemy import inspect
from app.bootstrap.container import container

# Helpers
def print_status(name, success, error=""):
    status = "[PASS]" if success else f"[FAIL] {error}"
    print(f"{name:.<40}{status}")
    if not success:
        sys.exit(1)

def test_memory_domain():
    try:
        mem = Memory(
            id="test-1",
            memory_type=MemoryType.PREFERENCE,
            content="I prefer testing.",
            importance=MemoryImportance.MEDIUM,
            created_at=datetime.utcnow()
        )
        
        # Test Immutability
        try:
            mem.content = "New content"
            print_status("1. Testing Memory Domain", False, "Memory is not immutable")
            return
        except FrozenInstanceError:
            pass
            
        # Test Enums
        assert mem.memory_type == MemoryType.PREFERENCE
        assert mem.importance == MemoryImportance.MEDIUM
        
        print_status("1. Testing Memory Domain", True)
    except Exception as e:
        print_status("1. Testing Memory Domain", False, str(e))

def test_memory_persistence():
    try:
        service = MemoryService()
        
        # Cleanup
        for m in service.get_all():
            service.delete(m.id)
            
        # Create
        mem1 = service.create(MemoryType.GOAL, "Test goal", MemoryImportance.HIGH)
        assert mem1 is not None
        
        # Retrieve after new service instance
        service2 = MemoryService()
        all_mems = service2.get_all()
        assert len(all_mems) == 1
        assert all_mems[0].content == "Test goal"
        
        # Duplicate allowed
        service2.create(MemoryType.GOAL, "Test goal", MemoryImportance.HIGH)
        all_mems_dup = service2.get_all()
        assert len(all_mems_dup) == 2
        
        # Delete existing
        deleted = service2.delete(mem1.id)
        assert deleted is True
        assert len(service2.get_all()) == 1
        
        # Delete unknown
        deleted_unknown = service2.delete("non-existent-id")
        assert deleted_unknown is False
        
        # Unknown lookup
        assert service2.get_by_id("non-existent-id") is None
        
        print_status("2. Testing Memory Persistence", True)
    except Exception as e:
        print_status("2. Testing Memory Persistence", False, str(e))

def test_memory_retrieval():
    try:
        service = MemoryService()
        # Cleanup
        for m in service.get_all():
            service.delete(m.id)
            
        service.create(MemoryType.PREFERENCE, "I prefer coding after dinner.", MemoryImportance.MEDIUM)
        service.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
        service.create(MemoryType.CONTEXT, "Working on Athena backend.", MemoryImportance.MEDIUM)
        
        retriever = MemoryRetriever(service)
        
        assert "coding after dinner" in retriever.retrieve("coding tonight").memories[0].content
        assert "Graduate this year" in retriever.retrieve("graduate thesis").memories[0].content
        assert "Athena backend" in retriever.retrieve("backend sprint").memories[0].content
        assert len(retriever.retrieve("vacation beach").memories) == 0
        
        # Punctuation normalization
        assert len(retriever.retrieve("Dinner.").memories) > 0 # Matches "dinner."
        assert len(retriever.retrieve("year!").memories) > 0 # Matches "year."
        
        print_status("3. Testing Memory Retrieval", True)
    except Exception as e:
        print_status("3. Testing Memory Retrieval", False, str(e))

async def test_memory_integration():
    try:
        service = container.memories
        
        # Cleanup
        for m in service.get_all():
            service.delete(m.id)
            
        # With Memory
        service.create(MemoryType.PREFERENCE, "I prefer coding after dinner.", MemoryImportance.MEDIUM)
        service.create(MemoryType.GOAL, "Graduate this year.", MemoryImportance.HIGH)
        
        briefing_with = await container.briefing.generate_daily_briefing()
        plan_with = await container.planning_service.generate_plan()
        advice_with = await container.advisor_service.advise("Can I game tonight?")
        
        assert len(briefing_with) > 0
        assert len(plan_with) > 0
        assert len(advice_with) > 0
        
        # Without Memory
        for m in service.get_all():
            service.delete(m.id)
            
        briefing_without = await container.briefing.generate_daily_briefing()
        plan_without = await container.planning_service.generate_plan()
        advice_without = await container.advisor_service.advise("Can I game tonight?")
        
        assert len(briefing_without) > 0
        assert len(plan_without) > 0
        assert len(advice_without) > 0
        
        # Advice outcome should be deterministic and remain unchanged (even though text changes)
        # We assume the router still blocks gaming tonight because there are tasks due today!
        # The prompt context logic was tested in PR 5. Here we just ensure no exceptions are thrown and output is valid.
        
        print_status("4. Testing Memory Integration", True)
    except Exception as e:
        print_status("4. Testing Memory Integration", False, str(e))

def test_existing_systems():
    try:
        resp_service = container.responsibilities
        projects_service = container.projects
        
        # Quick health checks
        all_resps = resp_service.get_all()
        assert isinstance(all_resps, list)
        
        all_projects = projects_service.get_all()
        assert isinstance(all_projects, list)
        
        plan = container.planner.generate_plan()
        assert plan is not None
        
        from app.time.duration import Duration
        workload = container.workload_balancer.analyze(Duration(minutes=120))
        assert workload is not None
        
        decision = container.question_router.route("Can I game tonight?")
        assert decision is not None
        
        print_status("5. Testing Existing Systems", True)
    except Exception as e:
        print_status("5. Testing Existing Systems", False, str(e))

def test_database_integrity():
    try:
        inspector = inspect(engine)
        
        # Ensure 'memories' table exists
        assert "memories" in inspector.get_table_names()
        
        # Check columns
        columns = [c['name'] for c in inspector.get_columns('memories')]
        assert "id" in columns
        assert "content" in columns
        assert "memory_type" in columns
        assert "importance" in columns
        assert "created_at" in columns
        
        print_status("6. Testing Database Integrity", True)
    except Exception as e:
        print_status("6. Testing Database Integrity", False, str(e))

async def async_main():
    print("\n--- Running Sprint 10 Regression Suite ---\n")
    test_memory_domain()
    test_memory_persistence()
    test_memory_retrieval()
    await test_memory_integration()
    test_existing_systems()
    test_database_integrity()
    print("\nALL TESTS PASSED!")
    print("Sprint 10 regression testing successful.\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(async_main())
