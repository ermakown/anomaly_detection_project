import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self):
        self._n_estimators: None | int = None
        self._contamination: None | float = None
        self._random_state: None | int = None
        self._data_predict: None | pd.DataFrame = None
        self._models: None | dict = dict()
        self._scalers: None | dict = dict()

    def fit(
        self,
        data: pd.DataFrame,
        resource: str,
        n_estimators=100,
        contamination=0.01,
        random_state=42,
    ) -> None:
        print(f'[INFO] Обучение модели для ресурса "{resource.title()}"...')

        self._n_estimators = n_estimators
        self._contamination = contamination
        self._random_state = random_state

        scaler = StandardScaler()
        X = data[["value"]]
        X_scale = scaler.fit_transform(X)
        self._scalers[resource] = scaler

        model = IsolationForest(
            n_estimators=self._n_estimators,
            contamination=self._contamination,
            random_state=self._random_state,
        )
        model.fit(X_scale)
        self._models[resource] = model

        print(f'[INFO] Для "{resource.title()}" модель успешно обучена.')

    def predict(self, data: pd.DataFrame, resource: str) -> None:
        print(f'[INFO] Предсказание аномалий для ресурса "{resource.title()}"')

        scaler = self._scalers.get(resource)
        model = self._models.get(resource)

        if not scaler or not model:
            raise ValueError(
                f'Обученной модели для "{resource.title()}" не существует.'
            )

        scaled_data = scaler.transform(data[["value"]])
        data["anomaly"] = model.predict(scaled_data)
        self._data_predict = data

        print("[INFO] Предсказание выполнено успешно.")

    @property
    def get_data(self) -> pd.DataFrame:
        return self._data_predict
