# Backend Dockerfile: FastAPI served by Gunicorn + Uvicorn workers.
#
# Single stage is enough here since we're not compiling anything heavy,
# but we still keep the image slim and run as a non-root user.

FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr,
# so logs show up immediately in `docker logs` / CloudWatch.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps needed to build psycopg2-binary's transitive deps on slim images.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user and switch to it.
RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 8000

# Gunicorn manages worker processes; each worker uses uvicorn's ASGI worker class.
# -w 2 is a sane default for a small learning-project instance size.
CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "2", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
