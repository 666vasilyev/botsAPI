DOCKER_COMPOSE=docker compose

all: clear compose-run

clear:
	@$(DOCKER_COMPOSE) down
	@$(DOCKER_COMPOSE) rm

compose-build:
	@$(DOCKER_COMPOSE) build -t bot-factory

compose-run: build
	@$(DOCKER_COMPOSE) up -d

compose-stop:
	@$(DOCKER_COMPOSE) stop

build:
	@env DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) build

build-test:
	@env DOCKER_BUILDKIT=1 $(DOCKER_COMPOSE) -f docker-compose-test.yaml build

pytest: build-test
	$(DOCKER_COMPOSE) -f docker-compose-test.yaml rm -f -s -v test-db
	$(DOCKER_COMPOSE) -f docker-compose-test.yaml up --remove-orphans
mypy:
	@mypy --ignore-missing-imports src tests

flake:
	@flake8 --per-file-ignores="__init__.py:F401" --ignore WPS301,WPS602,WPS115,E203,E501,W503,D100,D102,D103,D104,D101,WPS110,Q000,WPS226,S101,C812,WPS305,WPS300,I005,I001 src main.py tests

format:
	@echo "Форматирование"
	isort .
	black .
