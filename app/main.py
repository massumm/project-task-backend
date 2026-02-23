from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth,project,task, payment,admin

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(project.router)
app.include_router(auth.router)
app.include_router(task.router)
app.include_router(payment.router)
app.include_router(admin.router)