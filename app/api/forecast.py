from fastapi import APIRouter, HTTPException

from app.services.demand_forecast_engine import forecast_demand
from app.models.responses import ForecastResponse

router = APIRouter(prefix="/forecast", tags=["Demand Forecast"])


@router.get("/{sku}", response_model=ForecastResponse)
def get_demand_forecast(sku: str):
    """
    Forecast short-term demand for a SKU using recent sales trends.

    - Uses last 7 days of sales data
    - Predicts demand for the next 7 days
    - Flags stockout or dead stock risk
    """
    try:
        return forecast_demand(sku)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
