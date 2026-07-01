from devtools.models import PipelineRequest
from devtools.engine import PipelineEngine

def main():
    engine = PipelineEngine()
    
    print("--- Scenario 1: No Database ---")
    req1 = PipelineRequest(title="Sprint 10 (No DB)", touches_database=False)
    run1 = engine.plan(req1)
    for i, agent in enumerate(run1.planned_agents, 1):
        print(f"{i}. {agent.role} ({agent.name})")
        
    print("\n--- Scenario 2: Touches Database ---")
    req2 = PipelineRequest(title="Sprint 10 (DB)", touches_database=True)
    run2 = engine.plan(req2)
    for i, agent in enumerate(run2.planned_agents, 1):
        print(f"{i}. {agent.role} ({agent.name})")

if __name__ == "__main__":
    main()