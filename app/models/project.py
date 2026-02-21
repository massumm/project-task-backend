from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base
import uuid

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)