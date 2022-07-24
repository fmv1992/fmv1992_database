SHELL := /bin/bash -euo pipefail
export ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

export PROJECT ?= fmv1992_backup_system

export UID := $(shell id -u)
export GID := $(shell id -g)

DOCKER_COMPOSE_FILE := ./compose.yaml

# Postgres credentials. --- {{{

export POSTGRES_DB := fmv1992_backup_system
export POSTGRES_HOST := fmv1992_backup_system_postgres
export POSTGRES_PASSWORD := password_fmv1992_backup_system_postgres
export POSTGRES_USER := fmv1992_backup_system_user

#  --- }}}

all: format test

test: validate_docker_compose

format:
	DOCKER_CMD='bash -c '"'"'black .'"'" make docker_run
	DOCKER_CMD='sort -u -o requirements.txt -- requirements.txt' make docker_run
	DOCKER_CMD='python3 -m pip freeze | tr -d "\r" | sort -u | sponge requirements_all.txt' make docker_run

validate_docker_compose:
	docker-compose --file $(DOCKER_COMPOSE_FILE) config

# Docker. --- {{{

docker_build:
	docker-compose --file $(DOCKER_COMPOSE_FILE) build

docker_run:
	docker-compose \
        --file $(DOCKER_COMPOSE_FILE) \
        run \
        --rm \
        --entrypoint '' \
        fmv1992_backup_system_client \
        $(DOCKER_CMD)

docker_down:
	docker-compose --file $(DOCKER_COMPOSE_FILE) down --remove-orphans

docker_up:
	docker-compose --file $(DOCKER_COMPOSE_FILE) up --detach

docker_local_database_connect:
	DOCKER_CMD='env PGPASSWORD=$(POSTGRES_PASSWORD) psql --host $(POSTGRES_HOST) --username $(POSTGRES_USER) $(POSTGRES_DB)' make docker_run

#  --- }}}
