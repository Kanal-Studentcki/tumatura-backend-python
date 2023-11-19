format:
	poetry run isort .
	poetry run black .

format-check:
	poetry run isort . --check-only
	poetry run black . --check

mypy:
	poetry run mypy ./