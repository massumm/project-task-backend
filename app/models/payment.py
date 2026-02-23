from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id =Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    amount = Column(Float, nullable=False)
    status = Column(String, default="completed")  # simulate success