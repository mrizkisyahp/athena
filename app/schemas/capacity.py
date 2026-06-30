from pydantic import BaseModel

class CapacityAdvisorRequest(BaseModel):
    question: str

class CapacityAdvisorResponse(BaseModel):
    answer: str
