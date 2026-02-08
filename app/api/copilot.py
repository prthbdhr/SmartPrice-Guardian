from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.copilot import copilot_decision
from app.models.responses import CopilotResponse

router = APIRouter(prefix="/copilot", tags=["AI Copilot"])


class CopilotQuery(BaseModel):
    sku: str
    question: str


@router.post("/query", response_model=CopilotResponse)
def copilot_query(payload: CopilotQuery):
    """
    AI decision copilot for seller questions.

    Accepts a natural-language business question and returns
    a grounded, data-backed decision using:
    - Pricing intelligence
    - Demand forecast
    - Inventory signals
    - Market trends
    """
    try:
        return copilot_decision(payload.sku, payload.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
