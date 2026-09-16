"""
Insert example employees and tasks so the app has something to look at.

Run this AFTER migrations have created the tables:

    python seed.py

Safe to re-run: it checks for existing rows by email before inserting.
"""
from app.database.session import SessionLocal
from app.models.employee import Employee
from app.models.task import Task, TaskStatus

EMPLOYEES = [
    {"name": "John Carter", "email": "john.carter@example.com", "department": "Engineering"},
    {"name": "Sarah Lee", "email": "sarah.lee@example.com", "department": "HR"},
    {"name": "David Kim", "email": "david.kim@example.com", "department": "Finance"},
    {"name": "Priya Sharma", "email": "priya.sharma@example.com", "department": "Operations"},
]

TASKS = [
    {"title": "Set up CI pipeline", "description": "Configure GitHub Actions", "status": TaskStatus.IN_PROGRESS, "employee_email": "john.carter@example.com"},
    {"title": "Draft onboarding docs", "description": "Write new-hire onboarding guide", "status": TaskStatus.TODO, "employee_email": "sarah.lee@example.com"},
    {"title": "Close Q3 books", "description": "Reconcile Q3 financial statements", "status": TaskStatus.COMPLETED, "employee_email": "david.kim@example.com"},
    {"title": "Audit warehouse inventory", "description": "Cycle count for main warehouse", "status": TaskStatus.TODO, "employee_email": "priya.sharma@example.com"},
    {"title": "Review pull requests", "description": "Clear the backend PR queue", "status": TaskStatus.TODO, "employee_email": "john.carter@example.com"},
]


def run():
    db = SessionLocal()
    try:
        email_to_employee = {}
        for emp in EMPLOYEES:
            existing = db.query(Employee).filter(Employee.email == emp["email"]).first()
            if existing is None:
                existing = Employee(**emp)
                db.add(existing)
                db.commit()
                db.refresh(existing)
                print(f"Created employee: {existing.name}")
            email_to_employee[emp["email"]] = existing

        for t in TASKS:
            employee = email_to_employee[t["employee_email"]]
            existing_task = (
                db.query(Task)
                .filter(Task.title == t["title"], Task.employee_id == employee.id)
                .first()
            )
            if existing_task is None:
                task = Task(
                    title=t["title"],
                    description=t["description"],
                    status=t["status"],
                    employee_id=employee.id,
                )
                db.add(task)
                db.commit()
                print(f"Created task: {task.title}")
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
