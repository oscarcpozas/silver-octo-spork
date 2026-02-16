serve:
	uv run fastapi dev src/app.py

lint:
	uv run ruff check src/

migrate:
	docker compose run --rm flyway migrate

migrate-info:
	docker compose run --rm flyway info