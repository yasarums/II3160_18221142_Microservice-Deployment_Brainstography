import uvicorn
from fastapi import FastAPI
from app.client import router as client_router
from app.appointment import router as appointment_router
from app.progrep import router as progrep_router

app = FastAPI()

app.include_router(client_router, prefix = "/client")
app.include_router(appointment_router, prefix = "/appointment")
app.include_router(progrep_router, prefix = "/progrep")