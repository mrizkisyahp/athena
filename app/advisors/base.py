from abc import ABC, abstractmethod

from app.advisors.decision import AdvisorDecision


class BaseAdvisor(ABC):
    """
    Base class for all advisors.
    """

    @abstractmethod
    def supports(self, question: str) -> bool:
        """
        Returns True if this advisor can answer the question.
        """
        raise NotImplementedError

    @abstractmethod
    def advise(self, question: str) -> AdvisorDecision:
        """
        Produces a structured decision.
        """
        raise NotImplementedError
