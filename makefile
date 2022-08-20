SHELL := /bin/bash -euo pipefail
export ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

export PROJECT ?= fmv1992_database

export UID := $(shell id -u)
export GID := $(shell id -g)

DOCKER_COMPOSE_FILE := ./compose.yaml

# Postgres credentials. --- {{{

export POSTGRES_DB := fmv1992_database
export POSTGRES_HOST := fmv1992_database_postgres
export POSTGRES_PASSWORD := password_fmv1992_database_postgres
export POSTGRES_USER := fmv1992_database_user

#  --- }}}

define ensure_env_var_is_set
    @printenv $(1) >/dev/null 2>&1 || { echo 'Please define the `$(1)` env var.' >/dev/stderr && exit 1 ; }
endef

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
        fmv1992_database_client \
        $(DOCKER_CMD)

docker_down:
	docker-compose --file $(DOCKER_COMPOSE_FILE) down --remove-orphans

docker_up:
	docker-compose --file $(DOCKER_COMPOSE_FILE) up --detach

docker_local_database_connect:
	DOCKER_CMD='env PGPASSWORD=$(POSTGRES_PASSWORD) psql --host $(POSTGRES_HOST) --username $(POSTGRES_USER) $(POSTGRES_DB)' make docker_run

# Alembic. --- {{{

# `analytics_database_schemas:2396f2b:makefile:56`:
test_downgrade_upgrade:
	make docker_up
	sleep 5s
	DOCKER_CMD='env DB_USER=alembic_user bash -xv ./other/test/test_upgrade_then_downgrade.sh' make docker_run
	make down

alembic_autogenerate_upgrade:
	$(call ensure_env_var_is_set,POSTGRES_USER)
	$(call ensure_env_var_is_set,POSTGRES_PASSWORD)
	$(call ensure_env_var_is_set,POSTGRES_HOST)
	$(call ensure_env_var_is_set,POSTGRES_DB)
	$(call ensure_env_var_is_set,ALEMBIC_MESSAGE)
	DOCKER_CMD='./other/bin/alembic/alembic_auto_generate' make docker_run
	make format

alembic_upgrade:
	$(call ensure_env_var_is_set,POSTGRES_USER)
	$(call ensure_env_var_is_set,POSTGRES_PASSWORD)
	$(call ensure_env_var_is_set,POSTGRES_HOST)
	$(call ensure_env_var_is_set,POSTGRES_DB)
	$(call ensure_env_var_is_set,ALEMBIC_TARGET_ID)
	DOCKER_CMD='./other/bin/alembic/alembic_upgrade' make docker_run

alembic_downgrade:
	$(call ensure_env_var_is_set,POSTGRES_USER)
	$(call ensure_env_var_is_set,POSTGRES_PASSWORD)
	$(call ensure_env_var_is_set,POSTGRES_HOST)
	$(call ensure_env_var_is_set,POSTGRES_DB)
	$(call ensure_env_var_is_set,ALEMBIC_TARGET_ID)
	DOCKER_CMD='./other/bin/alembic/alembic_downgrade' make docker_run

#  --- }}}

#  --- }}}
