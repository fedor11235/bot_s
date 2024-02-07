include .env

VERSION=$$(git describe --always --tags)

dev:
 CONFIG_PATH=$(CONFIG_PATH) PYTHONPATH=./ poetry run python ./src/main/main.py

mypy:
 poetry run mypy src tests

flake:
 poetry run pflake8 src tests

pytest:
 poetry run pytest -vv -s --disable-warnings tests

format:
 @echo "Форматирование"
 poetry run isort --profile black .
 poetry run black .

check_imports:
 poetry run lint-imports
