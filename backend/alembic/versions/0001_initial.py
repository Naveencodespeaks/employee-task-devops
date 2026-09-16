"""initial tables: employees, tasks

Revision ID: 0001
Revises:
Create Date: 2026-01-01 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# PostgreSQL ENUM type.
# create_type=False means Alembic will not automatically try to
# CREATE TYPE while creating the tasks table.
task_status_enum = postgresql.ENUM(
    "TODO",
    "IN_PROGRESS",
    "COMPLETED",
    name="task_status",
    create_type=False,
)


def upgrade() -> None:
    # ---------------------------------------------------------
    # 1. Create employees table
    # ---------------------------------------------------------
    op.create_table(
        "employees",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),
        sa.Column(
            "name",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "department",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # Unique email address for every employee.
    op.create_index(
        "ix_employees_email",
        "employees",
        ["email"],
        unique=True,
    )

    # ---------------------------------------------------------
    # 2. Create PostgreSQL ENUM type
    # ---------------------------------------------------------
    task_status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    # ---------------------------------------------------------
    # 3. Create tasks table
    # ---------------------------------------------------------
    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),
        sa.Column(
            "title",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=2000),
            nullable=True,
        ),
        sa.Column(
            "status",
            task_status_enum,
            nullable=False,
            server_default="TODO",
        ),
        sa.Column(
            "employee_id",
            sa.Integer(),
            sa.ForeignKey(
                "employees.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # Index for quickly finding tasks belonging to an employee.
    op.create_index(
        "ix_tasks_employee_id",
        "tasks",
        ["employee_id"],
    )


def downgrade() -> None:
    # ---------------------------------------------------------
    # Remove tasks table
    # ---------------------------------------------------------
    op.drop_index(
        "ix_tasks_employee_id",
        table_name="tasks",
    )

    op.drop_table("tasks")

    # ---------------------------------------------------------
    # Remove PostgreSQL ENUM
    # ---------------------------------------------------------
    task_status_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )

    # ---------------------------------------------------------
    # Remove employees table
    # ---------------------------------------------------------
    op.drop_index(
        "ix_employees_email",
        table_name="employees",
    )

    op.drop_table("employees")