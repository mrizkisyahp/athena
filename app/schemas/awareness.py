from datetime import datetime
from pydantic import BaseModel


class InsightResponse(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    created_at: datetime
