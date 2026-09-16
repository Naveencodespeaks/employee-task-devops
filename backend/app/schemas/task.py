from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    employee_id: int


class TaskCreate(TaskBase):
    status: TaskStatus = TaskStatus.TODO


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    employee_id: int | None = None
    status: TaskStatus | None = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class DashboardOut(BaseModel):
    total_employees: int
    total_tasks: int
    todo_tasks: int
    in_progress_tasks: int
    completed_tasks: int
