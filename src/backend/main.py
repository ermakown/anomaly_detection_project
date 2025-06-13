from fastapi import FastAPI
from backend.back.api import api

app = FastAPI(title="Anomaly Detection API", version="1.0")

app.include_router(api.router)
