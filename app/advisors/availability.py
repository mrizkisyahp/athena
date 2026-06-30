from app.advisors.base import BaseAdvisor
from app.advisors.decision import AdvisorDecision, DecisionOutcome
from app.responsibilities.service import ResponsibilityService
from app.responsibilities.models import ResponsibilityPriority

class AvailabilityAdvisor(BaseAdvisor):

    def __init__(
        self,
        responsibilities: ResponsibilityService,
    ):
        self._responsibilities = responsibilities

    def supports(self, question: str) -> bool:
        normalized = question.lower()
        return (
            normalized.startswith("can i ")
            or "do i have time" in normalized
            or "am i free" in normalized
        )

    def _has_critical_today(self) -> bool:
        return any(
            r.priority == ResponsibilityPriority.CRITICAL
            for r in self._responsibilities.get_due_today()
        )

    def _has_overdue_high_priority(self) -> bool:
        return any(
            r.priority in (ResponsibilityPriority.HIGH, ResponsibilityPriority.CRITICAL)
            for r in self._responsibilities.get_overdue()
        )

    def _high_priority_count_today(self) -> int:
        return sum(
            1 for r in self._responsibilities.get_due_today()
            if r.priority == ResponsibilityPriority.HIGH
        )

    def advise(self, question: str) -> AdvisorDecision:
        reasoning = []

        if self._has_critical_today():
            reasoning.append("Critical work remains today.")
            return AdvisorDecision(
                outcome=DecisionOutcome.NO,
                confidence=0.95,
                reasoning=reasoning,
            )

        if self._has_overdue_high_priority():
            reasoning.append("High-priority overdue work exists.")
            return AdvisorDecision(
                outcome=DecisionOutcome.NO,
                confidence=0.95,
                reasoning=reasoning,
            )

        high_count = self._high_priority_count_today()
        if high_count > 1:
            reasoning.append("Today's workload is still significant.")
            return AdvisorDecision(
                outcome=DecisionOutcome.CONDITIONAL,
                confidence=0.85,
                reasoning=reasoning,
            )
        elif high_count == 1:
            reasoning.append("One important responsibility remains.")
            return AdvisorDecision(
                outcome=DecisionOutcome.CONDITIONAL,
                confidence=0.85,
                reasoning=reasoning,
            )

        reasoning.append("Remaining workload is manageable.")
        return AdvisorDecision(
            outcome=DecisionOutcome.YES,
            confidence=0.90,
            reasoning=reasoning,
        )
