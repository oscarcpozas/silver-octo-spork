serve:
	uv run fastapi dev src/app.py

lint:
	uv run ruff check src/