from app.advisors.router import QuestionRouter


class AdvisorService:

    def __init__(self, router: QuestionRouter):
        self._router = router
