# Water Intake Tracker Server Application - Exposed on a Rest API

A server application that exposes an API to track a person water intake. Built with Python, FastAPI, Prisma, and PostgreSQL, totally uncoupled and scalable by following the principles of Domain-Driven Design (DDD) / Hexagonal and Clean Architecture.

Some of techinical decisions were written as comments, directly in their respective files, in order to highlight it's advantages.

## Architecture (DDD)

The project is organized into three main layers:

| Layer               | Description                                                                                                |
|---------------------|------------------------------------------------------------------------------------------------------------|
| **domain/**         | Pure business rules. Entities, Value Objects, Repositories (interfaces), with no external dependencies.    |
| **application/**    | Application use cases, DTOs, orchestrating domain logic with infrastructure.                               | 
| **infrastructure/** | External communication: API (FastAPI), database (Prisma + PostgreSQL), logging, DI Container.              |
| **main.py**         | Application Entry Point                                                                                    |

The application code is set within the `src/` directory.

## Technologies

- Python 3.11
- FastAPI
- Prisma ORM
- PostgreSQL
- Docker + Docker Compose (Dev)
- Poetry (dependency and environment management)


## How to Run Locally (with Poetry)

### Requirements:

- Python 3.10+
- Poetry
- PostgreSQL

### Environment Setup:

1. Install dependencies:

```bash
poetry install
```

2. Create and configure a `.env` file at the project's root, with your `DATABASE_URL`. For instance, as set in `.env.example`:

```
DATABASE_URL=postgres://postgres:postgres@localhost:5432/water-intake-tracker-server-app
```

3. Generate the Prisma client:

```bash
poetry run prisma generate --schema=src/infrastructure/database/orm/prisma/schema.prisma
```

4. Generate migrations

```bash
poetry run prisma migrate dev --schema=src/infrastructure/database/orm/prisma/schema.prisma --name init
```

5. Run database migrations:

```bash
poetry run prisma migrate deploy --schema=src/infrastructure/database/orm/prisma/schema.prisma
```

### Running the API (Linux/macOS):

Navigate to the project directory (`cd`) and from the root folder, you can run the pre-configured startup script:

```bash
./run.sh
```

### Running on Windows (PowerShell):

Navigate to the project directory (`cd`) and from the root folder, you can run the pre-configured startup script:

```powershell
./run.ps1
```

If PowerShell blocks script execution, temporarily allow it with:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Available Services:

| Service           | URL                                                 |
|-------------------|-----------------------------------------------------|
| API               | http://localhost:8000                               |
| Swagger Docs      | http://localhost:8000/docs                          |



## Running with Docker Compose (Development)

### Build and start:

```bash
docker-compose -f docker-compose.dev.yml up --build
```


### Start (If closed after build):

```bash
docker-compose -f docker-compose.dev.yml up --remove-orphans
```

### Available Services:

| Service           | URL                                                 |
|-------------------|-----------------------------------------------------|
| API               | http://localhost:8000                               |
| Swagger Docs      | http://localhost:8000/docs                          |
| PostgreSQL        | localhost:5432 (user: postgres, password: postgres) |

The Prisma Client and migrations are automatically handled inside the container.

