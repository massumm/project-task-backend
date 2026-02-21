from app.core.database import engine, Base
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.payment import Payment

# Drop all tables
Base.metadata.drop_all(bind=engine)
print("All tables dropped successfully!")