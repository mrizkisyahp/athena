from pydantic import BaseModel


class AdvisorRequest(BaseModel):
    question: str


class AdvisorResponse(BaseModel):
    answer: str
