#!make
.PHONY: stories db_dump

include ./.env

DOCKER_COMPOSE_PROD = --env-file ./.env -f ./docker-compose.yml
DOCKER_COMPOSE_DEV = --env-file ./.env -f ./docker-compose-dev.yml
# DOCKER_COMPOSE_TESTS = --env-file ./.env -f ./docker-compose-dev.yml -f ./docker-compose-tests.yml

# Default, Help

# default: first_start_dev

help: # Вывод информации make командах
	@grep -E '^[a-zA-Z0-9 _-]+:.*#' Makefile | while read -r l; \
	do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Start, First start

first_start: postgres db_create stories_migrations

first_start_dev: postgres_dev db_create db_restore

start: prod

# Tests

first_start_tests: postgres_dev db_create db_restore

tests:
	docker compose $(DOCKER_COMPOSE_TESTS) up --build --attach tests

# Profiles

prod:
	docker compose $(DOCKER_COMPOSE_PROD) up -d

dev:
	docker compose $(DOCKER_COMPOSE_DEV) up -d --build --remove-orphans


# PostgreSQL

postgres:  # Собрать и запустить контейнер Postgres
	docker compose $(DOCKER_COMPOSE_PROD) up --build --force-recreate -d postgres

postgres_dev:  # Собрать и запустить контейнер Postgres
	docker compose $(DOCKER_COMPOSE_DEV) up --build --force-recreate -d postgres

db_dump: # Сделать дамп базы данных Postgres в файл ./db_dump/movies_db.backup
	docker compose $(DOCKER_COMPOSE_DEV) exec -i postgres bash -c "pg_dump -U $(POSTGRES_USER) -d postgres "\
	"-Fc -f /etc/db_dump/movies_db.backup $(POSTGRES_STORIES_DB)"

db_create: db_create_stories # Создать базы данных для сервисов

db_create_stories: # Создать базу данных для сервиса movies
	docker compose $(DOCKER_COMPOSE_DEV) exec -i postgres bash -c "/etc/db_dump/wait-for-postgres.sh localhost && "\
	"echo \"SELECT 'CREATE DATABASE $(POSTGRES_STORIES_DB)' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_STORIES_DB)')\gexec\" | psql -U $(POSTGRES_USER) -d postgres"

db_drop_stories: # Удалить базу данных для сервиса auth
	docker compose $(DOCKER_COMPOSE_DEV) exec -i postgres bash -c "/etc/db_dump/wait-for-postgres.sh localhost && "\
	"echo \"SELECT 'DROP DATABASE $(POSTGRES_AUTH_DB)' WHERE EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_AUTH_DB)')\gexec\" | psql -U $(POSTGRES_USER) -d postgres"

db_restore: # Восстановить базу данных Postgres из файла ./db_dump/movies_db.backup
	docker compose $(DOCKER_COMPOSE_DEV) exec -i postgres bash -c "/etc/db_dump/wait-for-postgres.sh localhost && "\
	"pg_restore -U $(POSTGRES_USER) -d postgres -Fc -c --if-exists -O -v --no-acl -d $(POSTGRES_MOVIES_DB) /etc/db_dump/movies_db.backup"


# Auth

stories:  # Собрать и запустить тестовый контейнер Auth (с зависимостями для разработки)
	docker compose $(DOCKER_COMPOSE_PROD) up --build -d stories

stories_dev:  # Собрать и запустить тестовый контейнер Auth (с зависимостями для разработки)
	docker compose $(DOCKER_COMPOSE_DEV) up --build -d stories

## make stories_upgrade_migration: команда для создания новой ревизии
stories_upgrade_migration:
	docker compose $(DOCKER_COMPOSE_PROD) run --rm --no-deps stories alembic revision --autogenerate -m "${MESSAGE}"

## make stories_migrations: команда для запуска всех миграций бд
stories_migrations:
	docker compose $(DOCKER_COMPOSE_PROD) run --rm auth alembic upgrade head

## make stories_downgrade_migration: команда для отката последней ревизии
stories_downgrade_migration:
	docker compose $(DOCKER_COMPOSE_PROD) run --rm auth alembic downgrade -1


# Stop & Down

stop:
	docker compose $(DOCKER_COMPOSE_PROD) stop

stop_dev:
	docker compose $(DOCKER_COMPOSE_DEV) stop

down:
	docker compose $(DOCKER_COMPOSE_PROD) down --remove-orphans

down_full:
	docker compose $(DOCKER_COMPOSE_PROD) down -v --rmi all --remove-orphans

clear: ## Команда для очистки всех контейнеров и образов (удалит вообще всё)
	docker system prune -a
	docker volume prune