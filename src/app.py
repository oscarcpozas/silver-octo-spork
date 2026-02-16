import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import get_settings
from src.market.router import router as market_router
from src.market.scheduler import ohlc_sync_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup: launch scheduler
    task = asyncio.create_task(ohlc_sync_loop())
    yield
    # Shutdown: cancel scheduler
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title=get_settings().project_name,
    lifespan=lifespan
)
app.include_router(market_router)


@app.get("/")
async def read_root():
    return {"status": "ok"}
