from fastapi import FastAPI
from app.api.data_summary import router as data_summary_router
from app.api.pricing import router as pricing_router

app = FastAPI(title="SmartPrice Guardian")

app.include_router(data_summary_router)
app.include_router(pricing_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
