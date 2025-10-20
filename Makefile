.PHONY: install dev lint format test coverage docker-up docker-down

install:
pip install -e .[dev]

dev:
flask --app app:create_app run --debug

lint:
ruff check app tests

format:
ruff check app tests --fix
black app tests
isort app tests

test:
pytest

coverage:
pytest --cov=app --cov-report=xml --cov-report=term

docker-up:
docker-compose up --build

docker-down:
docker-compose down -v

