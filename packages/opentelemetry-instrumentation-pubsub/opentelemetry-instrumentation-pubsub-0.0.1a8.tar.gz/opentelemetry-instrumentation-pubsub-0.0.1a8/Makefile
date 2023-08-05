SHELL := /bin/bash

.PHONY: install lint test format release build

install:
	pip install -e .[dev,test]

lint:
	flake8

test:
	pytest

build:
	python -m build

release: build
	twine upload dist/*

format:
	black pubsub_opentelemetry
	black tests
	isort pubsub_opentelemetry
	isort tests
