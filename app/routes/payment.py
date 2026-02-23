from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.payment import Payment
from app.models.task import Task
from app.models.project import Project
from app.schemas.payment import PaymentResponse
from app.dependencies.role_checker import role_required, get_current_user


router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/{task_id}", response_model=PaymentResponse)
def pay_for_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(role_required("buyer"))
):
    # Find task
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "submitted":
        raise HTTPException(status_code=400, detail="Task not ready for payment")

    # Verify buyer owns project
    project = db.query(Project).filter(
        Project.id == task.project_id,
        Project.buyer_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Calculate amount
    if not task.hours_spent:
        raise HTTPException(status_code=400, detail="Invalid hours")

    amount = task.hourly_rate * task.hours_spent

    # Create payment record
    payment = Payment(
        task_id=task.id,
        buyer_id=current_user.id,
        amount=amount,
        status="completed"
    )

    # Update task status
    task.status = "paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment