export_requirements:
	poetry export -f requirements.txt > requirements.txt --without-hashes

clean_pycache:
	find . -type d -name __pycache__ -exec rm -r {} \+

style:
	poetry run isort src/ tests/
	poetry run black src/ tests/
	poetry run flake8 src/ tests/
	poetry run flake8 *.md Makefile --select=W291
	poetry run mypy src/ tests/ --install-types --non-interactive --show-error-codes
	poetry run pylint src/ tests/

db_up:
	docker-compose up --build --force-recreate -d

db_create_tables:
	alembic upgrade head

db_add_migration:
	alembic revision --autogenerate -m "migration description"

run:
	export DB_HOST="localhost" && \
	export DB_DATABASE="shipay_users_db" && \
	export DB_USER="postgres" && \
	export DB_PASSWORD="postgres" && \
	poetry run gunicorn -w 2 -k uvicorn.workers.UvicornWorker --timeout 120 --chdir src main:app

debug:
	poetry run uvicorn --host 127.0.0.1 --port 8000 --reload --log-level debug --app-dir src main:app
