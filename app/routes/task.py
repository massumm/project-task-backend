from fastapi import APIRouter, Depends, HTTPException,UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse
from app.dependencies.role_checker import role_required, get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

#buyer creates task for a project
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(role_required("buyer"))
):
    #verify project belongs to buyer
    project = db.query(Project).filter(
        Project.id == task.project_id,
        Project.buyer_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by buyer")

    #veryfy assined user is developer
    developer = db.query(User).filter(
        User.id == task.assigned_developer,
        User.role == "developer"
    ).first()

    if not developer:
        raise HTTPException(status_code=404, detail="Assigned developer not found or not a developer")

    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        assigned_developer=task.assigned_developer,
        hourly_rate=task.hourly_rate
    )        
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#view task by project
@router.get("/project/{project_id}", response_model=List[TaskResponse])
def get_project_tasks(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.project_id == project_id).all()

    return tasks

#developer starts task
@router.post("/{task_id}/start", response_model=TaskResponse)
def start_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(role_required("developer"))
):
    task=db.query(Task).filter(
        Task.id == task_id,
        Task.assigned_developer == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not assigned to developer")

    task.status = "in_progress"
    db.commit()
    db.refresh(task)
    return task

#developer completes task
@router.post("/{task_id}/submit", response_model=TaskResponse)
def submit_task(
    task_id: str,
    hours_spent: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(role_required("developer"))
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.assigned_developer == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "in_progress":
        raise HTTPException(status_code=400, detail="Task not in progress")

    # Save file
    file_path = f"uploads/{task_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task.status = "submitted"
    task.hours_spent = hours_spent
    task.solution_file = file_path

    db.commit()
    db.refresh(task)

    return task

@router.get("/mine", response_model=List[TaskResponse])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role == "developer":
        tasks = db.query(Task).filter(
            Task.assigned_developer == current_user.id
        ).all()
    elif current_user.role == "buyer":
        tasks = db.query(Task).join(Project).filter(
            Project.buyer_id == current_user.id
        ).all()
    else:
        tasks = []
    
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Hide solution file unless paid
    if task.status != "paid":
        task.solution_file = None

    return task
