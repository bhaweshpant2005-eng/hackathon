
from pydantic import BaseModel
from typing import Optional, List

class TicketIn(BaseModel):
    subject: str
    description: str
    category: str = "general"
    priority: str = "medium"
    status: str = "open"
    assignee: Optional[str] = None

class TicketOut(BaseModel):
    id: str
    subject: str
    description: str
    category: str
    priority: str
    status: str
    created_by: str
    assignee: Optional[str] = None



