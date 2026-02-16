import logging

import httpx

from src.config import get_settings
from src.market.constants import BASE_URL, LIMIT, MULTIPLIER, TIMESPAN

logger = logging.getLogger(__name__)


async def fetch_ohlc_bars(
    ticker: str,
    from_ts: str,
    to_ts: str,
    http_client: httpx.AsyncClient,
) -> list[dict]:
    """Fetch OHLC bars from Massive API, following pagination if present."""
    all_results: list[dict] = []
    url: str | None = (
        f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/{MULTIPLIER}/{TIMESPAN}"
        f"/{from_ts}/{to_ts}"
    )
    params: dict | None = {
        "adjusted": "true",
        "sort": "asc",
        "limit": LIMIT,
        "apiKey": get_settings().massive_api_key,
    }

    while url:
        resp = await http_client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results") or []
        all_results.extend(results)
        logger.info(
            "Fetched %d bars for %s (total so far: %d)",
            len(results),
            ticker,
            len(all_results),
        )

        next_url = data.get("next_url")
        if next_url:
            # next_url is a full URL; append apiKey
            url = next_url
            params = {"apiKey": get_settings().massive_api_key}
        else:
            url = None

    return all_results
