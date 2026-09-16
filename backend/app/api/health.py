"""
Health endpoints used by Docker health checks, the ALB target group,
and Kubernetes liveness/readiness probes.

/health -> "is the process alive" (liveness). Never touches the DB.
/ready  -> "can this instance actually serve traffic" (readiness).
           Checks the database connection.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ready"}
