# database/init

This folder is intentionally empty of SQL scripts.

Table creation is handled by **Alembic migrations** (`backend/alembic/`),
not by scripts dropped into Postgres's `/docker-entrypoint-initdb.d/`.
That keeps schema changes versioned and reviewable in Git, and avoids the
classic "the container auto-created tables and now migrations conflict
with reality" problem.

If you ever need one-time database bootstrapping unrelated to the app's
schema (e.g. creating extensions), you can add `.sql` files here and
mount this directory into the postgres service in `docker-compose.yml`:

```yaml
postgres:
  volumes:
    - ./database/init:/docker-entrypoint-initdb.d
```
