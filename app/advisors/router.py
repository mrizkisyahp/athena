from app.advisors.base import BaseAdvisor


class QuestionRouter:
    """
    Routes a question to the appropriate advisor.
    """

    def __init__(self, advisors: list[BaseAdvisor]):
        self._advisors = advisors

    def route(self, question: str) -> BaseAdvisor | None:
        for advisor in self._advisors:
            if advisor.supports(question):
                return advisor

        return None
