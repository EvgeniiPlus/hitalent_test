from fastapi import FastAPI
from app.routers import tables, reservations
from app.db.session import engine
from app.models import models
from app.core.logger import setup_logging

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Restaurant Reservation API',
    version='1.0.0'
)

setup_logging()

app.include_router(tables.router, prefix='/tables', tags=['Tables'])
app.include_router(reservations.router, prefix='/reservations', tags=['Reservations'])