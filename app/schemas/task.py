from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class TaskCreate(BaseModel):
    project_id: UUID
    title: str
    description: str
    assigned_developer: UUID
    hourly_rate: float\

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    hourly_rate: float
    hours_spent: Optional[float]
    solution_file: Optional[str]
    project_id: UUID
    assigned_developer: UUID


    class Config:
        from_attributes = True  