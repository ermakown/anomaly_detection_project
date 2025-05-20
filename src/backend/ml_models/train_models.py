from preprocessing import DataPrepare
from anomaly_detection import AnomalyDetector
import matplotlib.pyplot as plt

ex = DataPrepare(
    "C:/Users/Vladimir/Desktop/anomaly_detection_project/src/backend/ml_data_input/electricity_data_prepared.csv"
)
ex.load_data()
ex.prepare()
# print(ex.data.head())
# print(ex.data.dtypes)

model = AnomalyDetector()
model.fit(ex.data, "электричество")
model.predict(ex.data, "электричество")

df = ex.data
anomalies = df[df["anomaly"] == -1]

target_date = "2007-01-02"
daily_data = df[df["Date"] == target_date].copy()
daily_anomalies = daily_data[daily_data["anomaly"] == -1]


plt.figure(figsize=(15, 6))
plt.plot(
    df["Datetime"],
    df["value"],
    label="потребление",
    color="black",
    alpha=0.7,
)
plt.scatter(
    anomalies["Datetime"],
    anomalies["value"],
    c="red",
    marker="o",
    label="аномалии",
)

plt.show()
