from pydantic import BaseModel
from typing import List


class PricingResponse(BaseModel):
    sku: str
    current_price: float
    recommended_price: float
    decision: str
    confidence: float
    reason: str


class ForecastResponse(BaseModel):
    sku: str
    forecast_window_days: int
    predicted_demand: int
    current_stock: int
    risk: str
    explanation: str


class CopilotResponse(BaseModel):
    sku: str
    decision: str
    answer: str
    confidence: float
    signals_used: List[str]
