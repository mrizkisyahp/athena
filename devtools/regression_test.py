from pathlib import Path
from devtools.config import EngineeringTeam
from devtools.engine import PipelineEngine
from devtools.models import PipelineRequest, PipelineRun, PipelineReport
from devtools.history import RunHistory

def test_configuration():
    print("1. Testing Configuration...")
    agents = EngineeringTeam.get_all_agents()
    assert len(agents) == 6, f"Expected 6 configured agents, got {len(agents)}"
    
    roles = {a.role for a in agents}
    expected_roles = {"Technical Lead", "Development Orchestrator", "Architect", "Backend Executor", "Database Reviewer", "QA Reviewer"}
    assert roles == expected_roles, "Missing required roles"
    
    db_reviewer = next(a for a in agents if a.role == "Database Reviewer")
    assert db_reviewer.is_conditional is True, "Database Reviewer must be conditional"
    print("[PASS] Configuration valid")

def test_prompt_discovery():
    print("2. Testing Prompt Discovery...")
    prompt_dir = Path("devtools/prompts")
    prompts = list(prompt_dir.glob("*.md"))
    
    # We expect 5 prompts (excluding Technical Lead which is human-owned)
    assert len(prompts) == 5, f"Expected exactly 5 prompts, found {len(prompts)}"
    
    expected_files = {
        "architect.md",
        "executor.md",
        "db_reviewer.md",
        "qa_reviewer.md",
        "antigravity.md"
    }
    
    found_files = {p.name for p in prompts}
    assert found_files == expected_files, f"Prompt files mismatch: {found_files}"
    
    print("[PASS] Prompt discovery valid")

def test_pipeline_planning():
    print("3. Testing Pipeline Planning...")
    engine = PipelineEngine()
    
    # Scenario A
    req_a = PipelineRequest(title="Scenario A", touches_database=False)
    run_a = engine.plan(req_a)
    roles_a = [a.role for a in run_a.planned_agents]
    assert roles_a == ["Architect", "Backend Executor", "QA Reviewer"], "Scenario A execution order failed"
    
    # Scenario B
    req_b = PipelineRequest(title="Scenario B", touches_database=True)
    run_b = engine.plan(req_b)
    roles_b = [a.role for a in run_b.planned_agents]
    assert roles_b == ["Architect", "Backend Executor", "Database Reviewer", "QA Reviewer"], "Scenario B execution order failed"
    
    print("[PASS] Pipeline planning valid")

def test_run_history():
    print("4. Testing Run History...")
    history = RunHistory()
    
    run1 = PipelineRun(name="Run 1", planned_agents=[], report=PipelineReport("Done", True, "Summary 1"))
    run2 = PipelineRun(name="Run 2", planned_agents=[], report=PipelineReport("Done", True, "Summary 2"))
    
    history.add(run1)
    history.add(run2)
    
    assert history.get("Run 1") == run1
    assert history.get("Run 2") == run2
    assert len(history.get_all()) == 2
    
    print("[PASS] Run history valid")

def test_reports():
    print("5. Testing Reports...")
    run = PipelineRun(name="Run", planned_agents=[], report=PipelineReport(stage="Implementation", completed=True, summary="Testing report"))
    
    assert run.report is not None, "PipelineRun must contain exactly one PipelineReport"
    assert isinstance(run.report, PipelineReport)
    
    print("[PASS] Reports valid")

def run_tests():
    test_configuration()
    test_prompt_discovery()
    test_pipeline_planning()
    test_run_history()
    test_reports()
    
    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
