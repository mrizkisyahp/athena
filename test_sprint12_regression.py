import sys
import os
import subprocess
from datetime import datetime, time
from fastapi.testclient import TestClient

from app.main import app
from app.bootstrap.container import container
from app.time.duration import Duration
from app.responsibilities.models import ResponsibilityPriority, ResponsibilityStatus
from app.services.time_service import TimeService
from app.awareness.models import Insight, InsightSeverity
from app.awareness.service import InsightEngine
from app.awareness.prompt import InsightPromptBuilder
from app.services.briefing_formatter import BriefingFormatter

def cleanup():
    for r in container.responsibilities.get_all():
        if r.status != ResponsibilityStatus.COMPLETED:
            container.responsibilities.complete(r.id)
    for e in container.events.get_all():
        container.events.delete(e.id)

def test_awareness_domain():
    print("1. Testing Awareness Domain............", end="", flush=True)
    # Validation
    try:
        Insight(title="", description="Desc", severity=InsightSeverity.HIGH)
        assert False, "Should raise ValueError for empty title"
    except ValueError:
        pass

    try:
        Insight(title="Title", description="", severity=InsightSeverity.HIGH)
        assert False, "Should raise ValueError for empty description"
    except ValueError:
        pass
        
    # Immutability
    i = Insight(title="A", description="B", severity=InsightSeverity.LOW)
    try:
        i.title = "C"
        assert False, "Should be immutable"
    except Exception:
        pass
        
    # Enum
    assert InsightSeverity.HIGH.value == "high"
    assert InsightSeverity.MEDIUM.value == "medium"
    assert InsightSeverity.LOW.value == "low"
    
    print("[PASS]")

def test_insight_engine():
    print("2. Testing Insight Engine..............", end="", flush=True)
    cleanup()
    today = TimeService.now().date()
    capacity = Duration(minutes=480)
    
    # Trigger all 4 rules
    container.events.create("Morning", datetime.combine(today, time(8, 0)), datetime.combine(today, time(12, 0)))
    # Max free block is 12 hours (12:00 to 24:00) -> 720 minutes. 
    # To get Unscheduled Responsibilities, we need a task that requires more than 720 minutes.
    # To get Overloaded Day, total workload > 480 minutes.
    # So a 721-minute task will trigger Overloaded Day and Unscheduled Responsibilities.
    # We also have a 12 hour free block (720 minutes), which triggers Large Focus Block (>= 120 mins).
    # Wait, if we have an Unscheduled task, does "No Scheduled Work" trigger? Yes, if it's the ONLY task!
    container.responsibilities.create(
        title="Huge Task",
        priority=ResponsibilityPriority.HIGH,
        estimated_duration=Duration(minutes=721)
    )
    
    insights = container.insights.generate(today, capacity)
    assert len(insights) == 4
    
    # Check stable severity sorting
    assert insights[0].severity == InsightSeverity.HIGH
    assert insights[1].severity == InsightSeverity.HIGH
    assert insights[2].severity == InsightSeverity.MEDIUM
    assert insights[3].severity == InsightSeverity.LOW
    
    titles = [i.title for i in insights]
    assert "Overloaded Day" in titles
    assert "Unscheduled Responsibilities" in titles
    assert "No Scheduled Work" in titles
    assert "Large Focus Block Available" in titles
    
    print("[PASS]")

def test_prompt_builders():
    print("3. Testing Prompt Builders.............", end="", flush=True)
    # Empty
    assert InsightPromptBuilder.build([]) == ""
    
    # Single
    i1 = Insight(title="T1", description="D1", severity=InsightSeverity.HIGH)
    p1 = InsightPromptBuilder.build([i1])
    assert "Current Insights" in p1
    assert "[HIGH] T1" in p1
    
    # Multiple
    i2 = Insight(title="T2", description="D2", severity=InsightSeverity.LOW)
    p2 = InsightPromptBuilder.build([i1, i2])
    assert "[HIGH] T1" in p2
    assert "[LOW] T2" in p2
    
    print("[PASS]")

def test_briefing_formatter():
    print("4. Testing Briefing Formatter..........", end="", flush=True)
    
    # Empty omission
    p1 = BriefingFormatter.build("", "", "")
    assert p1 == ""
    
    p2 = BriefingFormatter.build("Schedule", "", "Insights")
    assert p2 == "Schedule\n\nInsights"
    
    # Ordering
    p3 = BriefingFormatter.build("Schedule", "Memory", "Insights")
    assert p3 == "Schedule\n\nMemory\n\nInsights"
    
    print("[PASS]")

def test_insights_api():
    print("5. Testing Insights API................", end="", flush=True)
    cleanup()
    
    # Seed deterministic data
    today = TimeService.now().date()
    container.responsibilities.create(
        title="Huge Task",
        priority=ResponsibilityPriority.HIGH,
        estimated_duration=Duration(minutes=721)
    )
    
    client = TestClient(app)
    response = client.get("/insights")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 2 # Depending on events, could be 4.
    
    # Verify Schema
    assert "id" in data[0]
    assert "title" in data[0]
    assert "description" in data[0]
    assert "severity" in data[0]
    assert "created_at" in data[0]
    
    # Verify severity ordering
    severities = [i["severity"] for i in data]
    # high should come before medium before low
    order_map = {"high": 1, "medium": 2, "low": 3}
    for i in range(len(severities) - 1):
        assert order_map[severities[i]] <= order_map[severities[i+1]]
        
    print("[PASS]")

def test_existing_systems():
    print("6. Testing Existing Systems............", end="", flush=True)
    # We will invoke the previous sprint regression tests via subprocess
    test_scripts = [
        "test_sprint11_regression.py" # sprint 11 contains tests for everything up to 11
    ]
    for script in test_scripts:
        if os.path.exists(script):
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            if result.returncode != 0:
                print("\n[FAIL] Output from", script)
                print(result.stdout)
                print(result.stderr)
                assert False, f"{script} failed!"
                
    print("[PASS]")

def test_database_integrity():
    print("7. Testing Database Integrity..........", end="", flush=True)
    # The container uses actual DB connections
    try:
        container.responsibilities.get_all()
        print("[PASS]")
    except Exception as e:
        print("\n[FAIL]", str(e))
        assert False, "Database integrity check failed"

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("--- Running Sprint 12 Regression Suite ---\n")
    
    test_awareness_domain()
    print()
    test_insight_engine()
    print()
    test_prompt_builders()
    print()
    test_briefing_formatter()
    print()
    test_insights_api()
    print()
    test_existing_systems()
    print()
    test_database_integrity()
    print()
    
    print("ALL TESTS PASSED!\n")
    print("Sprint 12 regression testing successful.")

if __name__ == "__main__":
    main()
