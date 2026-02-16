import asyncio
import logging

from src.market.constants import SYNC_INTERVAL_SECONDS
from src.market.service import sync_all_tickers

logger = logging.getLogger(__name__)


async def ohlc_sync_loop() -> None:
    """Run OHLC sync immediately, then every SYNC_INTERVAL_SECONDS."""
    while True:
        logger.info("Starting OHLC sync cycle...")
        try:
            results = await sync_all_tickers()
            total = sum(v for v in results.values() if v > 0)
            logger.info("OHLC sync complete — %d new bars total", total)
        except Exception:
            logger.exception("Unhandled error in OHLC sync cycle")

        await asyncio.sleep(SYNC_INTERVAL_SECONDS)
