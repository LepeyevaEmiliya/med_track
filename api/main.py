from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.routes import appointments
from infrastructure.database import DatabasePool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabasePool.get_pool()
    yield
    await DatabasePool.close_pool()


app = FastAPI(
    title="MedTrack API",
    lifespan=lifespan
)

app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])