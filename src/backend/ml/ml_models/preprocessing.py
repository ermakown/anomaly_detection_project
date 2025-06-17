import pandas as pd


class DataPrepare:
    def __init__(self):
        self._path: None | str = None
        self.data: None | pd.DataFrame = None

    def load_data(self, path: str) -> None:
        self._path = path
        print("[INFO] Выполняется загрузка данных из файлов...")

        self.data = pd.read_csv(self._path)
        if isinstance(self.data, pd.DataFrame):
            print(
                f"[INFO] Данные успешно загружены: {self.data.shape[0]} строк, {self.data.shape[1]} столбцов."
            )
        else:
            raise ValueError(
                "Возникла ошибка при считывании данных из файла. Проверьте данные и повторите попытку."
            )

    def prepare(self) -> None:
        self.data["Datetime"] = pd.to_datetime(
            self.data["Date"] + " " + self.data["Time"]
        )
        self.data = self.data.sort_values("Datetime")

        if "Global_active_power" in self.data.columns:
            self.data.rename(columns={"Global_active_power": "value"}, inplace=True)
        elif "Water_Consumption" in self.data.columns:
            self.data.rename(columns={"Water_Consumption": "value"}, inplace=True)
        elif "Gas_Consumption" in self.data.columns:
            self.data.rename(columns={"Gas_Consumption": "value"}, inplace=True)
        else:
            raise ValueError(
                "Данные не содержат нужного столбца с показателями. Проверьте данные и повторите попытку."
            )

        print(
            "[INFO] Обработка и подготовка данных завершены. Данные готовы к обучению модели."
        )

    def drop_column(self, column: str) -> None:
        if column in self.data.columns:
            del self.data[column]
        else:
            raise ValueError(
                f'Столбца "{column}" не существует в наборе данных.'
            )

    @property
    def get_data(self) -> pd.DataFrame:
        return self.data
