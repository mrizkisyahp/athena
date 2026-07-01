import sys
from devtools.models import PipelineRequest
from devtools.engine import PipelineEngine
from devtools.providers.nine_router import NineRouterProvider
from devtools.runtime import ExecutionRuntime
from devtools.history import RunHistory
from devtools.orchestrator import PipelineOrchestrator

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Setup Infrastructure
    engine = PipelineEngine()
    provider = NineRouterProvider()
    runtime = ExecutionRuntime(provider=provider)
    history = RunHistory()
    
    orchestrator = PipelineOrchestrator(
        engine=engine, 
        runtime=runtime, 
        history=history
    )
    
    # Execute Workflow
    print("Starting Orchestrator Workflow for Sprint 10 PR 2...")
    request = PipelineRequest(title="Sprint 10 PR2: Memory Service", touches_database=False)
    
    instructions = """
Target Project: Athena
Sprint: 10
PR: #2
Feature: Memory Service

Objective: Implement the domain service responsible for managing Athena's long-term memories.

Requirements:
Create `app/memory/service.py`.
Implement `MemoryService` with the following responsibilities:
1. `create(memory_type: MemoryType, content: str, importance: MemoryImportance) -> Memory`: Creates and stores a new memory.
2. `get_all() -> list[Memory]`: Returns every stored memory.
3. `get_by_id(memory_id: str) -> Memory | None`: Returns a specific memory.
4. `delete(memory_id: str) -> bool`: Deletes a memory (returns True if deleted, False if not found).
5. `get_by_type(memory_type: MemoryType) -> list[Memory]`: Returns memories matching the category.

Business Rules:
- No uniqueness constraints. Duplicate content (e.g., Preference "I like coffee" twice) is allowed.
- Memory represents observations, not normalized DB records.

Storage:
- Use purely in-memory storage (e.g., `self._memories: list[Memory]`).
- No PostgreSQL/ORM logic yet.
- Return pure domain objects.

Special Requests for the DevTools Pipeline:
- ARCHITECT: Consider whether deleting a memory should physically remove it, or if Athena should eventually support archiving. Note your thoughts in the review, but recommend physical deletion for this PR.
- QA: Specifically verify that creating multiple memories of the same type works, duplicate content is allowed, get_by_id() returns None for unknown IDs, delete() returns False when ID doesn't exist, and the service doesn't mutate existing Memory instances (since they are immutable).

Playground:
Create several memories (Preference, Goal, Routine, Context).
Verify: All Memories -> Get by Type -> Get by ID -> Delete -> Verify deletion.
"""
    
    run = orchestrator.execute_pipeline(request, instructions=instructions)
    
    # Save Pipeline Results to a file so Antigravity can read it easily
    with open("pipeline_report.md", "w", encoding="utf-8") as f:
        f.write(f"--- Pipeline Complete ---\n")
        f.write(f"Stages Executed: {len(run.results)} / {len(run.planned_agents)}\n")
        total_duration = sum(r.duration_seconds for r in run.results if r.duration_seconds)
        f.write(f"Duration: {total_duration:.2f}s\n")
        status = "PASS" if run.report.completed else "FAIL"
        f.write(f"Status: {status}\n")
        f.write(f"Summary: {run.report.summary}\n\n")
        for result in run.results:
            f.write(f"[{result.agent.role}]\n")
            f.write(f"{result.output.strip()}\n\n")
            
    print("Pipeline output saved to pipeline_report.md")

if __name__ == "__main__":
    main()