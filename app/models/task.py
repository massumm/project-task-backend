from sqlalchemy import Column, String, Float, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    assigned_developer = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    hourly_rate = Column(Float, nullable=False)
    status = Column(String, default="todo")

    hours_spent = Column(Float, nullable=True)
    solution_file = Column(String, nullable=True)
    
    project = relationship("Project")
    developer = relationship("User")