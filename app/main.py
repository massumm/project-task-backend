from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth, project, task, payment, admin

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router)
app.include_router(auth.router)
app.include_router(task.router)
app.include_router(payment.router)
app.include_router(admin.router)