serve:
	uv run fastapi dev src/app.py

lint:
	uv run ruff check src/

test:
	APP_ENV=test uv run --group test pytest tests/ -v

migrate:
	docker compose run --rm flyway migrate

migrate-info:
	docker compose run --rm flyway info