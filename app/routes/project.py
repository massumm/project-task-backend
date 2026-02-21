from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.dependencies.role_checker import role_required, get_current_user
from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse)
def create_project(
    project:ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(role_required("buyer"))
):
    new_project =Project(
        title=project.title,
        description=project.description,
        buyer_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/mine", response_model=List[ProjectResponse])
def get_my_projects(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    projects = db.query(Project).filter(
        Project.buyer_id == current_user.id
    ).all()

    return projects