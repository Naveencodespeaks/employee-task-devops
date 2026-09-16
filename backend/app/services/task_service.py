from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate, DashboardOut


def list_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.id).all()


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, data: TaskCreate) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        employee_id=data.employee_id,
        status=data.status,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()


def get_dashboard_stats(db: Session) -> DashboardOut:
    total_employees = db.query(func.count(Employee.id)).scalar() or 0
    total_tasks = db.query(func.count(Task.id)).scalar() or 0

    def count_by_status(status: TaskStatus) -> int:
        return db.query(func.count(Task.id)).filter(Task.status == status).scalar() or 0

    return DashboardOut(
        total_employees=total_employees,
        total_tasks=total_tasks,
        todo_tasks=count_by_status(TaskStatus.TODO),
        in_progress_tasks=count_by_status(TaskStatus.IN_PROGRESS),
        completed_tasks=count_by_status(TaskStatus.COMPLETED),
    )
