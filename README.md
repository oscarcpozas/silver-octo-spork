## Set up

This project uses [uv](https://docs.astral.sh/uv) as a package/project manager.

```bash
uv run fastapi dev
```

uv run will automatically resolve and lock the project dependencies (i.e., create a uv.lock alongside the pyproject.toml), create a virtual environment, and run the command in that environment.