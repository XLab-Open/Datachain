# Makefile for Datachain project

.PHONY: help install install-dev test test-unit test-integration test-slow test-cov test-html clean lint format type-check

# Default target
help:
	@echo "Available commands:"
	@echo "  install        - Install production dependencies"
	@echo "  install-dev    - Install development dependencies"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-slow      - Run slow tests only"
	@echo "  test-cov       - Run tests with coverage"
	@echo "  test-html      - Generate HTML coverage report"
	@echo "  lint           - Run linting checks"
	@echo "  clean          - Clean up generated files"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest

test-unit:
	pytest -m "not integration and not slow"

test-integration:
	pytest -m integration

test-slow:
	pytest -m slow

test-cov:
	pytest --cov=datachain --cov-report=term-missing

test-html:
	pytest --cov=datachain --cov-report=html
	@echo "HTML coverage report generated in htmlcov/index.html"

# Code quality
lint:
	pre-commit run --all-files

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
