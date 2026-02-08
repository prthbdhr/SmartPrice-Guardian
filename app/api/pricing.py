from fastapi import APIRouter, HTTPException

from app.services.pricing_engine import pricing_decision
from app.models.responses import PricingResponse

router = APIRouter(prefix="/pricing", tags=["Pricing"])


@router.get("/recommendation/{sku}", response_model=PricingResponse)
def get_pricing_recommendation(sku: str):
    """
    Get an AI-driven pricing recommendation for a SKU.

    This decision considers:
    - Recent sales behavior
    - Current inventory levels
    - Competitor pricing signals

    Returns a clear pricing action with reasoning and confidence.
    """
    try:
        return pricing_decision(sku)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
