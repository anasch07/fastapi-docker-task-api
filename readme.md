# FastAPI Task Management API

## Project Overview

This project is a simple task management API built with Python using the **FastAPI** framework. It allows users to create and retrieve tasks through a RESTful API. The application is containerized using Docker and orchestrated with Docker Compose, consisting of two services:

- **api**: The FastAPI application.
- **db**: A PostgreSQL database with persistent data volume.

The project is managed with **Poetry** for dependency management and uses **Alembic** for database migrations.

## Features

- **API Endpoints**:
  - `GET /tasks`: Fetch all tasks.
  - `POST /tasks`: Create a new task.
- **Task Model**:
  - `id`: Integer, unique identifier for the task.
  - `name`: String, name of the task.
  - `completion_status`: Boolean, indicates if the task is completed.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### Build and Run the Application

Use the provided **Makefile** to build and start the application:

```bash
make up
```

This command will:

- Build the Docker images.
- Start both the `api` and `db` services defined in `docker-compose.yml`.

Alternatively, you can use Docker Compose directly:

```bash
docker-compose up --build
```

### Access the API

The API will be accessible at `http://localhost:8000`.

## API Documentation

Interactive API documentation is available via Swagger UI:

- Open your web browser and navigate to `http://localhost:8000/docs`.

## API Endpoints

### GET /tasks

Retrieve all tasks.

- **URL**: `/tasks`
- **Method**: `GET`
- **Response**: A JSON array of task objects.

**Example Request**

```bash
curl -X GET http://localhost:8000/tasks
```

**Example Response**

```json
[
  {
    "id": 1,
    "name": "First Task",
    "completion_status": false
  },
  {
    "id": 2,
    "name": "Second Task",
    "completion_status": true
  }
]
```

### POST /tasks

Create a new task.

- **URL**: `/tasks`
- **Method**: `POST`
- **Request Body**: A JSON object with `name` and `completion_status`.

**Example Request**

```bash
curl -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{
           "name": "New Task",
           "completion_status": false
         }'
```

**Example Response**

```json
{
  "id": 3,
  "name": "New Task",
  "completion_status": false
}
```


## Dependency Management

The project uses **Poetry** for dependency management.

- **pyproject.toml**: Contains project metadata and dependencies.
- **poetry.lock**: Locks the versions of the dependencies.

### Installing Dependencies Manually

If you need to install dependencies manually (outside of Docker), you can use Poetry:

```bash
poetry install
```

## Database Migrations

The project uses **Alembic** for database migrations.

### Generating Migrations

To generate a new migration after modifying models, use the Makefile command:

```bash
make migrate
```

Or directly with Docker Compose:

```bash
docker-compose exec api alembic revision --autogenerate -m "Migration message"
```

### Applying Migrations

To apply migrations, use:

```bash
make migrate
```

Or:

```bash
docker-compose exec api alembic upgrade head
```

**Note**: The initial migration is already created and applied when you start the application with Docker Compose.

## Running Tests

Unit tests are included in the `tests/` directory. To run the tests, use:

```bash
make test
```

This command will:

- Run the tests using `pytest`.
- Use a test database to avoid affecting the development database.

Alternatively, you can run:

```bash
poetry run pytest
```

### Test Coverage

Ensure that your code is properly tested by running the tests after making changes.

## Stopping the Application

To stop the application and remove containers, networks, and volumes, use:

```bash
make down
```

Or directly:

```bash
docker-compose down
```

- This will stop the containers but **will not** delete the persistent data volume for PostgreSQL.

## Persistent Data Volume

- The PostgreSQL database uses a Docker volume (`postgres_data`) to persist data.
- Data will not be lost when bringing the containers down and up again.
- To delete the data volume (and all data), run:

  ```bash
  docker-compose down --volumes
  ```

