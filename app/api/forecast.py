from fastapi import APIRouter, HTTPException

from app.services.demand_forecast_engine import forecast_demand

router = APIRouter(prefix="/forecast", tags=["Demand Forecast"])


@router.get("/{sku}")
def get_demand_forecast(sku: str):
    """
    Demand forecast endpoint.
    Delegates all computation to the forecast engine.
    """
    try:
        return forecast_demand(sku)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
