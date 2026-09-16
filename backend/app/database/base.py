"""
Shared declarative base class.

Every model (Employee, Task, ...) inherits from this `Base` so that
Alembic's autogenerate can discover all tables via `Base.metadata`.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
