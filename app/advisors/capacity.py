import re
from app.advisors.base import BaseAdvisor
from app.advisors.decision import AdvisorDecision, DecisionOutcome
from app.planning.service import ExecutionPlanner
from app.time.capacity import CapacityRequest
from app.time.duration import Duration


class CapacityAdvisor(BaseAdvisor):
    def __init__(self, planner: ExecutionPlanner):
        self._planner = planner

    def supports(self, question: str) -> bool:
        q = question.lower()
        return bool(re.search(r'(\d+)\s*(min|minute|minutes|hr|hour|hours|h|m)\b', q))

    def _parse_duration(self, question: str) -> Duration | None:
        match = re.search(r'(\d+)\s*(min|minute|minutes|hr|hour|hours|h|m)\b', question.lower())
        if not match:
            return None
            
        value = int(match.group(1))
        unit = match.group(2)
        
        if unit.startswith('h'):
            return Duration(value * 60)
        return Duration(value)

    def advise(self, question: str) -> AdvisorDecision:
        duration = self._parse_duration(question)
        if not duration:
            return AdvisorDecision(
                outcome=DecisionOutcome.CONDITIONAL,
                confidence=0.0,
                reasoning=["I couldn't parse the exact amount of time you have available."]
            )
            
        request = CapacityRequest(available_time=duration)
        plan = self._planner.generate_plan()
        
        if plan.total_estimated_duration is None:
            return AdvisorDecision(
                outcome=DecisionOutcome.CONDITIONAL,
                confidence=1.0,
                reasoning=["Some responsibilities are missing time estimates. Athena cannot accurately determine whether your available time is sufficient."]
            )
            
        if request.available_time.minutes >= plan.total_estimated_duration.minutes:
            return AdvisorDecision(
                outcome=DecisionOutcome.YES,
                confidence=1.0,
                reasoning=[f"Today's planned work is estimated at {plan.total_estimated_duration.hours:g} hours. You currently have {request.available_time.hours:g} hours available. Your available time is sufficient."]
            )
            
        return AdvisorDecision(
            outcome=DecisionOutcome.NO,
            confidence=1.0,
            reasoning=[f"Today's planned work is estimated at {plan.total_estimated_duration.hours:g} hours, but you only have {request.available_time.hours:g} hours available."]
        )
