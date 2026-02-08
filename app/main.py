from fastapi import FastAPI

app = FastAPI(title="SmartPrice Guardian")

@app.get("/health")
def health_check():
    return {"status": "ok"}
