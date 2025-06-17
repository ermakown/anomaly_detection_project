from fastapi import FastAPI
from backend.back.api import api

app = FastAPI(title="Noma API", version="1.0")

app.include_router(api.router)
