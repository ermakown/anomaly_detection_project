from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.database.db import AsyncSessionLocal
from backend.database import crud
from backend.ml.ml_models.preprocessing import DataPrepare
from backend.ml.ml_models.anomaly_detection import AnomalyDetector
from sqlalchemy import delete, select
import pandas as pd

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), resource: str = Form(...)) -> dict:
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))

        dp = DataPrepare()
        dp.data = df
        dp.prepare()
        df = dp.get_data

        async with AsyncSessionLocal() as session:
            await session.execute(
                delete(crud.RawMeasurement).where(
                    crud.RawMeasurement.resource == resource
                )
            )
            await session.execute(
                delete(crud.Measurement).where(crud.Measurement.resource == resource)
            )
            await session.commit()

            await crud.save_raw_data(session, df, resource)

            detector = AnomalyDetector()
            detector.fit(df, resource)
            detector.predict(df, resource)
            df = detector.get_data

            await crud.save_detected_anomalies(session, df, resource)

        return {
            "status": "success",
            "message": f"Файл успешно обработан для ресурса '{resource}'.",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/anomalies")
async def get_anomalies(resource: str) -> dict:
    async with AsyncSessionLocal() as session:
        anomalies = await crud.get_anomalies_by_resource(session, resource)
        result = [
            {
                "datetime": str(row["datetime"]),
                "value": row["value"],
                "resource": row["resource"],
            }
            for row in anomalies
        ]
        return {"resource": resource, "anomalies": result}


@router.get("/measurements")
async def get_measurements(resource: str) -> list:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(crud.Measurement).where(crud.Measurement.resource == resource)
        )
        return [
            {
                "datetime": row.datetime.isoformat(),
                "value": row.value,
                "resource": row.resource,
                "is_anomaly": row.is_anomaly
            }
            for row in result.scalars().all()
        ]
