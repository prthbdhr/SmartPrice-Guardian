from fastapi import APIRouter

from app.services.market_trends import get_market_trend

router = APIRouter(prefix="/market", tags=["Market Trends"])


@router.get("/trends")
def get_trends():
    return get_market_trend(category="electronics")
