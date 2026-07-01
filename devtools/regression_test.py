from pathlib import Path
from devtools.config import EngineeringTeam, Profiles, ProfileRegistry
from devtools.prompt_library import PromptLibrary
from devtools.engine import PipelineEngine
from devtools.models import PipelineRequest, PipelineRun, PipelineReport, AgentResult
from devtools.history import RunHistory
from devtools.reporting import ReportBuilder
from devtools.runtime import ExecutionRuntime
from devtools.providers.base import BaseProvider
from devtools.providers.nine_router import NineRouterProvider
from devtools.providers.models import ProviderRequest, ProviderResponse
from devtools.orchestrator import PipelineOrchestrator

class FakeProvider(BaseProvider):
    def execute(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            output=f"Fake output for {request.agent.role}",
            provider_name="FakeProvider",
            duration_seconds=0.1
        )

class FailingFakeProvider(BaseProvider):
    def execute(self, request: ProviderRequest) -> ProviderResponse:
        raise RuntimeError("Simulated provider failure")

def test_configuration():
    print("1. Testing Configuration...")
    agents = EngineeringTeam.get_all_agents()
    assert len(agents) == 6, f"Expected 6 configured agents, got {len(agents)}"
    
    # Verify profiles resolve
    registry = ProfileRegistry()
    for agent in agents:
        profile = registry.resolve(agent)
        assert profile is not None, f"Profile missing for {agent.name}"
        
    print("[PASS] Configuration valid")

def test_prompt_discovery():
    print("2. Testing Prompt Discovery...")
    library = PromptLibrary()
    agents = EngineeringTeam.get_all_agents()
    
    for agent in agents:
        # Technical Lead is human, but we ensure get_prompt doesn't crash
        prompt = library.get_prompt(agent)
        assert prompt, f"Prompt should not be empty for {agent.name}"
        if agent.role != "Technical Lead":
            # Just ensuring it didn't use the fallback unless necessary
            # We know antigravity.md exists, architect.md exists, etc.
            assert not prompt.startswith("You are a"), f"Prompt fallback triggered for {agent.name}"
            
    print("[PASS] Prompt discovery valid")

def test_pipeline_planning():
    print("3. Testing Pipeline Planning...")
    engine = PipelineEngine()
    
    req_a = PipelineRequest(title="Scenario A", touches_database=False)
    run_a = engine.plan(req_a)
    roles_a = [a.role for a in run_a.planned_agents]
    assert roles_a == ["Architect", "Backend Executor", "QA Reviewer"], "Scenario A execution order failed"
    
    req_b = PipelineRequest(title="Scenario B", touches_database=True)
    run_b = engine.plan(req_b)
    roles_b = [a.role for a in run_b.planned_agents]
    assert roles_b == ["Architect", "Backend Executor", "Database Reviewer", "QA Reviewer"], "Scenario B execution order failed"
    
    print("[PASS] Pipeline planning valid")

def test_runtime_fake():
    print("4. Testing Runtime (FakeProvider)...")
    provider = FakeProvider()
    runtime = ExecutionRuntime(provider=provider)
    engine = PipelineEngine()
    run = engine.plan(PipelineRequest(title="Test", touches_database=False))
    
    runtime.execute(run, "Test instructions")
    assert len(run.results) == 3
    assert run.results[0].agent.role == "Architect"
    assert "Fake output" in run.results[0].output
    
    print("[PASS] Runtime verified with FakeProvider")

def test_ninerouter_smoke():
    print("5. Testing NineRouter Smoke Test...")
    agent = EngineeringTeam.ARCHITECT
    profile = ProfileRegistry.resolve(agent)
    
    # Skip if FAKE to allow offline tests to pass if NineRouter isn't configured for Architect
    if profile.provider_type == "fake":
        print("[SKIP] NineRouter smoke test skipped (Architect uses FAKE profile)")
        return
        
    request = ProviderRequest(
        agent=agent,
        profile=profile,
        instructions="Return the exact word 'OK'",
        prompt="You are a test agent."
    )
    
    provider = NineRouterProvider()
    response = provider.execute(request)
    assert response.provider_name == "NineRouter"
    assert response.duration_seconds > 0
    assert response.output
    
    print("[PASS] NineRouter smoke test valid")

def test_orchestrator():
    print("6. Testing Orchestrator...")
    engine = PipelineEngine()
    provider = FakeProvider()
    runtime = ExecutionRuntime(provider=provider)
    history = RunHistory()
    
    orchestrator = PipelineOrchestrator(engine, runtime, history)
    run = orchestrator.execute_pipeline(PipelineRequest(title="Orchestrator Test"), "instructions")
    
    assert len(run.results) == 3
    assert run.report.completed is True
    assert history.get("Orchestrator Test") == run
    
    print("[PASS] Orchestrator verified")

def test_failure_path():
    print("7. Testing Failure Path...")
    engine = PipelineEngine()
    provider = FailingFakeProvider()
    runtime = ExecutionRuntime(provider=provider)
    history = RunHistory()
    
    orchestrator = PipelineOrchestrator(engine, runtime, history)
    run = orchestrator.execute_pipeline(PipelineRequest(title="Failure Test"), "instructions")
    
    assert len(run.results) == 0  # Halted on first step
    assert run.report.completed is False
    assert "Simulated provider failure" in run.report.summary
    assert history.get("Failure Test") == run
    
    print("[PASS] Failure path verified")

def test_report_validation():
    print("8. Testing Report Validation...")
    # This is implicitly tested inside test_orchestrator and test_failure_path
    # but we can explicitly test ReportBuilder here
    run = PipelineRun(name="Test Run")
    run.planned_agents = [EngineeringTeam.ARCHITECT]
    
    success_report = ReportBuilder.success(run)
    assert success_report.completed is True
    
    failure_report = ReportBuilder.failure(run, Exception("Test Error"))
    assert failure_report.completed is False
    assert "Test Error" in failure_report.summary
    
    print("[PASS] Report validation verified")

def run_tests():
    test_configuration()
    test_prompt_discovery()
    test_pipeline_planning()
    test_runtime_fake()
    test_ninerouter_smoke()
    test_orchestrator()
    test_failure_path()
    test_report_validation()
    
    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
