all: test

test: validate_docker_compose

validate_docker_compose:
	docker-compose -f ./docker_compose.yml config
