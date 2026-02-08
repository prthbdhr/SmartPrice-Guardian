from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.copilot import copilot_decision

router = APIRouter(prefix="/copilot", tags=["AI Copilot"])


class CopilotQuery(BaseModel):
    sku: str
    question: str


@router.post("/query")
def copilot_query(payload: CopilotQuery):
    try:
        return copilot_decision(payload.sku, payload.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
