from fastapi import APIRouter, HTTPException

from app.services.pricing_engine import pricing_decision

router = APIRouter(prefix="/pricing", tags=["Pricing"])


@router.get("/recommendation/{sku}")
def get_pricing_recommendation(sku: str):
    """
    Pricing recommendation endpoint.
    Delegates all decision-making to the pricing engine.
    """
    try:
        return pricing_decision(sku)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
