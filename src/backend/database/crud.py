from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database.models import RawMeasurement, Measurement
from typing import List
import pandas as pd


async def save_raw_data(session: AsyncSession, df: pd.DataFrame, resource: str) -> None:
    records = [
        RawMeasurement(datetime=row["Datetime"], resource=resource, value=row["value"])
        for _, row in df.iterrows()
    ]
    session.add_all(records)
    await session.commit()


async def save_detected_anomalies(
    session: AsyncSession, df: pd.DataFrame, resource: str
) -> None:
    records = [
        Measurement(
            datetime=row["Datetime"],
            resource=resource,
            value=row["value"],
            is_anomaly=row["anomaly"] == -1,
        )
        for _, row in df.iterrows()
    ]
    session.add_all(records)
    await session.commit()


async def get_anomalies_by_resource(session: AsyncSession, resource: str) -> List[dict]:
    result = await session.execute(
        select(Measurement).where(
            Measurement.resource == resource, Measurement.is_anomaly == True
        )
    )
    return [
        {
            "datetime": row.datetime.isoformat(),
            "value": row.value,
            "resource": row.resource,
        }
        for row in result.scalars().all()
    ]
