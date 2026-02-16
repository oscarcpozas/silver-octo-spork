from sqlalchemy import func, select
from fastapi import APIRouter, Query

from src.database import async_session
from src.market.constants import TICKERS
from src.market.models import OHLCBar
from src.market.schemas import OHLCBarOut, TickerStatus

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/tickers")
async def list_tickers() -> list[str]:
    return TICKERS


@router.get("/bars/{ticker:path}", response_model=list[OHLCBarOut])
async def get_bars(
    ticker: str,
    limit: int = Query(default=100, ge=1, le=5000),
) -> list[OHLCBarOut]:
    async with async_session() as session:
        result = await session.execute(
            select(OHLCBar)
            .where(OHLCBar.ticker == ticker)
            .order_by(OHLCBar.timestamp.desc())
            .limit(limit)
        )
        return [OHLCBarOut.model_validate(row) for row in result.scalars().all()]


@router.get("/status", response_model=list[TickerStatus])
async def sync_status() -> list[TickerStatus]:
    statuses: list[TickerStatus] = []
    async with async_session() as session:
        for ticker in TICKERS:
            result = await session.execute(
                select(
                    func.count(OHLCBar.id),
                    func.min(OHLCBar.timestamp),
                    func.max(OHLCBar.timestamp),
                ).where(OHLCBar.ticker == ticker)
            )
            count, earliest, latest = result.one()
            statuses.append(
                TickerStatus(
                    ticker=ticker,
                    bar_count=count,
                    earliest=earliest,
                    latest=latest,
                )
            )
    return statuses
