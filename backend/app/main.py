from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import employees, tasks, dashboard, health
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging(settings.environment)

app = FastAPI(
    title="Employee Task Management API",
    description="Simple 3-tier DevOps learning project backend.",
    version="1.0.0",
)

# CORS: the frontend runs on a different origin (different port/domain),
# so the browser needs this to allow the requests through.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(employees.router)
app.include_router(tasks.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"service": "employee-task-backend", "docs": "/docs"}
