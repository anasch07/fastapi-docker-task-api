DOCKER_COMPOSE = docker compose
PROJECT_DIR = fastapi-docker-app

# Commands
.PHONY: help build up down migrate test

help:
	@echo "Available commands:"
	@echo "  make build     - Build the Docker images"
	@echo "  make up        - Start the application using Docker Compose"
	@echo "  make down      - Stop the application and remove containers"
	@echo "  make migrate   - Apply database migrations"
	@echo "  make test      - Run unit tests"

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up --build

down:
	$(DOCKER_COMPOSE) down

migrate:
	cd $(PROJECT_DIR) && $(DOCKER_COMPOSE) exec api alembic upgrade head

test:
	cd $(PROJECT_DIR) && poetry run pytest
