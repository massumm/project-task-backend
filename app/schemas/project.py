from pydantic import BaseModel
from uuid import UUID

class ProjectCreate(BaseModel):
    title: str
    description: str
class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: str
    buyer_id: UUID

    class Config:
        from_attributes  = True    
