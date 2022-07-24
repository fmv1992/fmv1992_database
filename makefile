SHELL := /bin/bash -euo pipefail
export ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

export PROJECT ?= fmv1992_backup_system

export UID := $(shell id -u)
export GID := $(shell id -g)

DOCKER_COMPOSE_FILE := ./compose.yaml

all: format test

test: validate_docker_compose

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

format:
	DOCKER_CMD='bash -c '"'"'black .'"'" make docker_run
	DOCKER_CMD='sort -u -o requirements.txt -- requirements.txt' make docker_run
	DOCKER_CMD='python3 -m pip freeze | tr -d "\r" | sort -u | sponge requirements_all.txt' make docker_run

validate_docker_compose:
	docker-compose --file $(DOCKER_COMPOSE_FILE) config
