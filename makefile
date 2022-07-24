SHELL := /bin/bash -euo pipefail
export ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

export PROJECT ?= fmv1992_backup_system

export UID := $(shell id -u)
export GID := $(shell id -g)

DOCKER_COMPOSE_FILE := ./compose.yaml

all: test

test: validate_docker_compose

docker_build:
	docker-compose --file $(DOCKER_COMPOSE_FILE) build

validate_docker_compose:
	docker-compose --file $(DOCKER_COMPOSE_FILE) config
