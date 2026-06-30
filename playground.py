from app.advisors.availability import AvailabilityAdvisor
from app.advisors.decision import DecisionOutcome
from app.responsibilities.models import Responsibility, ResponsibilityPriority

class MockResponsibilityService:
    def __init__(self):
        self.due_today = []
        self.overdue = []

    def get_due_today(self):
        return self.due_today

    def get_overdue(self):
        return self.overdue

def main():
    service = MockResponsibilityService()
    advisor = AvailabilityAdvisor(service)
    q = "Can I game tonight?"

    # Scenario 1: Critical task today -> NO
    service.due_today = [Responsibility(title="test", priority=ResponsibilityPriority.CRITICAL)]
    service.overdue = []
    decision = advisor.advise(q)
    assert decision.outcome == DecisionOutcome.NO, f"Expected NO, got {decision.outcome}"
    print("Scenario 1: PASS")

    # Scenario 2: Overdue high task -> NO
    service.due_today = []
    service.overdue = [Responsibility(title="test", priority=ResponsibilityPriority.HIGH)]
    decision = advisor.advise(q)
    assert decision.outcome == DecisionOutcome.NO, f"Expected NO, got {decision.outcome}"
    print("Scenario 2: PASS")

    # Scenario 3: One high task today -> CONDITIONAL
    service.due_today = [Responsibility(title="test", priority=ResponsibilityPriority.HIGH)]
    service.overdue = []
    decision = advisor.advise(q)
    assert decision.outcome == DecisionOutcome.CONDITIONAL, f"Expected CONDITIONAL, got {decision.outcome}"
    print("Scenario 3: PASS")

    # Scenario 4: Only low/medium tasks -> YES
    service.due_today = [Responsibility(title="test", priority=ResponsibilityPriority.MEDIUM)]
    service.overdue = []
    decision = advisor.advise(q)
    assert decision.outcome == DecisionOutcome.YES, f"Expected YES, got {decision.outcome}"
    print("Scenario 4: PASS")

if __name__ == "__main__":
    main()