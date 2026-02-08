from fastapi import FastAPI
from app.api.data_summary import router as data_summary_router
from app.api.pricing import router as pricing_router
from app.api.forecast import router as forecast_router
from app.api.copilot import router as copilot_router
from app.api.market_trends import router as market_trends_router



app = FastAPI(title="SmartPrice Guardian")

app.include_router(data_summary_router)
app.include_router(pricing_router)
app.include_router(forecast_router)
app.include_router(copilot_router)
app.include_router(market_trends_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
