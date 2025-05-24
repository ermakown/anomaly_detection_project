from fastapi import FastAPI
from backend.back.api import anomalies

app = FastAPI(
    title="Anomaly Detection API",
    version="1.0"
)

app.include_router(anomalies.router)
