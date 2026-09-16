from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def list_employees(db: Session) -> list[Employee]:
    return db.query(Employee).order_by(Employee.id).all()


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    employee = Employee(name=data.name, email=data.email, department=data.department)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee: Employee, data: EmployeeUpdate) -> Employee:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee: Employee) -> None:
    db.delete(employee)
    db.commit()
