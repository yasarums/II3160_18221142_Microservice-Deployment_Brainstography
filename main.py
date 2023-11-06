from fastapi import FastAPI
from client import router as client_router
from appointment import router as appointment_router
from progrep import router as progrep_router
from reservation import router as reservation_router

app = FastAPI()

app.include_router(client_router, prefix = "/client")
app.include_router(appointment_router, prefix = "/appointment")
app.include_router(progrep_router, prefix = "/progrep")
app.include_router(reservation_router, prefix = "/reservation")