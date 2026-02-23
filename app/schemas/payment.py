from pydantic import BaseModel
from uuid import UUID

class PaymentResponse(BaseModel):
    id: UUID
    task_id: UUID
    buyer_id: UUID
    amount: float
    status: str

    class Config:
        from_attributes = True