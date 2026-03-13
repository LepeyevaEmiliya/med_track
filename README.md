# MedTrack API

A REST API for managing medical appointments, patient measurements, and prescriptions. Built with FastAPI and PostgreSQL.

## Tech Stack

- **Python 3.13**
- **FastAPI** — web framework
- **asyncpg** — async PostgreSQL driver
- **PostgreSQL** — primary database
- **Pydantic** — data validation
- **Uvicorn** — ASGI server

## Architecture

The project follows a **layered architecture** with strict separation of concerns:

```
HTTP Request
     ↓
API Layer (FastAPI routes + Pydantic schemas)
     ↓
Domain Layer (services + business logic)
     ↓
Infrastructure Layer (repositories + DB)
```

Key principles applied:
- **SOLID** — each class has a single responsibility, dependencies are injected via constructors
- **Repository pattern** — domain layer never touches the database directly
- **DTO pattern** — data transfer objects separate API layer from domain
- **Domain exceptions** — `PatientNotFoundError`, `InvalidDosageError` etc. instead of generic exceptions

## Database Schema

```sql
users         — base user accounts (id, name, email, role, created_at)
patients      — patient profiles (user_id FK, birth_date)
doctors       — doctor profiles (user_id FK, specialization)
appointments  — doctor-patient appointments (doctor_id FK, patient_id FK, time, status)
prescriptions — medication prescriptions (doctor_id FK, patient_id FK, medication, complaints)
measurements  — patient health measurements (patient_id FK, systolic, diastolic, glucose, measured_at)
```

## API Endpoints

### Appointments

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/appointments/` | Create a new appointment |
| `GET` | `/appointments/` | List all appointments |
| `GET` | `/appointments/{id}` | Get appointment by ID |
| `DELETE` | `/appointments/{id}` | Delete appointment |

## Key Implementation Details

**Custom decorators** (`domain/decorators.py`):
- `@log_call` — logs function name, arguments, execution time
- `@require_role(*roles)` — role-based access control
- `@retry(times, exceptions)` — automatic retry for external API calls

**Async repositories** — all database operations use `asyncpg` connection pool with `async/await`. Repositories implement `IReadableRepository` and `IWritableRepository` interfaces.

**Notification system** — uses a metaclass registry pattern. Each notification type (`EmailNotification`, `SMSNotification`) auto-registers itself in `NOTIFICATION_REGISTRY` on class creation.

**Validators** — blood pressure format (`120/80`), dosage (`500 mg`), appointment dates validated before reaching the database.


## What's Planned

- [ ] JWT authentication
- [ ] Celery + RabbitMQ for async reminders
- [ ] Redis caching for measurements dashboard
- [ ] Docker Compose setup
- [ ] Alembic migrations
