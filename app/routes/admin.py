from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.payment import Payment
from app.dependencies.role_checker import role_required, get_current_user


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_platform_stats(
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin"))
):
    # Total Users
    total_users = db.query(func.count(User.id)).scalar()

    # Total Projects
    total_projects = db.query(func.count(Project.id)).scalar()

    # Total Tasks
    total_tasks = db.query(func.count(Task.id)).scalar()

    # Tasks by Status
    status_counts = db.query(
        Task.status,
        func.count(Task.id)
    ).group_by(Task.status).all()

    tasks_by_status = {status: count for status, count in status_counts}

    # Total Revenue (only completed payments)
    total_revenue = db.query(
        func.coalesce(func.sum(Payment.amount), 0)
    ).filter(Payment.status == "completed").scalar()

    # Total Paid Developer Hours
    total_paid_hours = db.query(
        func.coalesce(func.sum(Task.hours_spent), 0)
    ).filter(Task.status == "paid").scalar()

    return {
        "total_users": total_users,
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "tasks_by_status": tasks_by_status,
        "total_revenue": total_revenue,
        "total_paid_hours": total_paid_hours
    }