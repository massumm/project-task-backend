from sqlalchemy import Column, String, Float, ForeignKey
from app.core.database import Base
import uuid

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    assigned_developer = Column(String, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    hourly_rate = Column(Float)
    status = Column(String, default="todo")
    hours_spent = Column(Float, nullable=True)
    solution_file = Column(String, nullable=True)