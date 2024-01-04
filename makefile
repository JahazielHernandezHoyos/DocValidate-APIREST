# Makefile for Dockerized Django with Poetry

# Variables
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_FILE := docker/compose.yaml
DOCKER_COMPOSE_FILE_DEBUG := docker/compose-debug.yaml

# Targets
.PHONY: build up down clean migrations superuser start

debug-mode-start:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE_DEBUG) up

build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up

down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

clean:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down -v --remove-orphans

migrations:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api python app/manage.py makemigrations
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api python app/manage.py migrate

superuser:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api python app/manage.py createsuperuser --username=admin --email=admin@example.com

start:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d --build
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api python app/manage.py migrate

create-app:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec api python app/manage.py startapp $(name)
