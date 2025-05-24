import asyncio
from sqlalchemy import delete
from backend.database.db import AsyncSessionLocal
from backend.database import crud
from backend.ml.ml_models.preprocessing import DataPrepare
from backend.ml.ml_models.anomaly_detection import AnomalyDetector

CSV_PATH = (
    "C:/Users/Vladimir/Desktop/anomaly_detection_project/src/backend/ml/ml_data_input/electricity_data_prepared.csv"
    )
RESOURCE = "electricity"


async def main():
    print("[INFO] Загружаем и подготавливаем данные...")

    dp = DataPrepare()
    dp.load_data(CSV_PATH)
    dp.prepare()
    df = dp.get_data
    print(f"[DEBUG] Загружено строк: {len(df)}")

    async with AsyncSessionLocal() as session:
        print(f"[INFO] Удаляем старые данные для ресурса: {RESOURCE}")
        await session.execute(
            delete(crud.RawMeasurement).where(crud.RawMeasurement.resource == RESOURCE)
        )
        await session.execute(
            delete(crud.Measurement).where(crud.Measurement.resource == RESOURCE)
        )
        await session.commit()
        print("[INFO] Старые данные удалены.")

        print("[INFO] Сохраняем новые исходные данные в БД...")
        await crud.save_raw_data(session, df, RESOURCE)

        print("[INFO] Обучаем модель...")
        detector = AnomalyDetector()
        detector.fit(df, RESOURCE)
        detector.predict(df, RESOURCE)
        df = detector.get_data
        print(f"[DEBUG] Строк после предсказания: {len(df)}")

        print("[INFO] Сохраняем аномалии в БД...")
        await crud.save_detected_anomalies(session, df, RESOURCE)

        anomalies = await crud.get_anomalies_by_resource(session, RESOURCE)
        print(f"[RESULT] Найдено аномалий: {len(anomalies)}")
        for row in anomalies[:5]:
            print(row)


if __name__ == "__main__":
    asyncio.run(main())
