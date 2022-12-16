DIRS := skupper_prometheus_collector tests
BUILD_ARGS := POETRY_VERSION=1.2.2

IMAGE_NAME := quay.io/app-sre/skupper-prometheus-collector
IMAGE_TAG := $(shell git rev-parse --short=7 HEAD)
DOCKER_CONF := ${PWD}/.docker

format:
	poetry run black $(DIRS)
	poetry run isort $(DIRS)
.PHONY: format

pr-check:
	docker build -t skupper-prometheus-collector-test -f Dockerfile.test --progress plain $(foreach arg,$(BUILD_ARGS),--build-arg $(arg)) .
.PHONY: pr-check

test:
	poetry run pytest -vv
	poetry run flake8 $(DIRS)
	poetry run mypy $(DIRS)
	poetry run black --check $(DIRS)
	poetry run isort --check-only $(DIRS)
.PHONY: test

build-deploy:
	docker build -t "${IMAGE_NAME}:latest" -f Dockerfile --progress plain $(foreach arg,$(BUILD_ARGS),--build-arg $(arg)) .
	docker tag "${IMAGE_NAME}:latest" "${IMAGE_NAME}:${IMAGE_TAG}"

	mkdir -p "${DOCKER_CONF}"
	docker --config="${DOCKER_CONF}" login -u="${QUAY_USER}" -p="${QUAY_TOKEN}" quay.io

	docker --config="${DOCKER_CONF}" push "${IMAGE_NAME}:latest"
	docker --config="${DOCKER_CONF}" push "${IMAGE_NAME}:${IMAGE_TAG}"
.PHONY: build-deploy
