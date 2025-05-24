import asyncio
from src.backend.database.db import engine, Base
from models import Measurement, RawMeasurement


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())
