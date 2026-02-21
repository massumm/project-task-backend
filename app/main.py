from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)