import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self, n_estimators=100, contamination=0.01, random_state=42):
        self.n_estimators = n_estimators
        self.contamination = contamination
        self.random_state = random_state
        self.models = dict()
        self.scalers = dict()

    def fit(self, data: pd.DataFrame, resource: str) -> None:
        print(f'[INFO] Обучение модели для ресурса "{resource.title()}"...')

        scaler = StandardScaler()
        X = data[["value"]]
        X_scale = scaler.fit_transform(X)
        self.scalers[resource] = scaler

        model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=self.random_state,
        )
        model.fit(X_scale)
        self.models[resource] = model
        print(f'[INFO] Для "{resource.title()}" модель успешно обучена.')

    def predict(self, data: pd.DataFrame, resource: str) -> None:
        print(f'[INFO] Предсказание аномалий для ресурса "{resource.title()}"')

        scaler = self.scalers.get(resource)
        model = self.models.get(resource)

        if not scaler or not model:
            raise ValueError(
                f'Обученной модели для "{resource.title()}" не существует.'
            )

        scaled_data = scaler.transform(data[["value"]])
        data["anomaly"] = model.predict(scaled_data)

        print("[INFO] Предсказание выполнено успешно.")
        return data
