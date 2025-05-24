from preprocessing import DataPrepare
from anomaly_detection import AnomalyDetector
import matplotlib.pyplot as plt

ex = DataPrepare()
ex.load_data(
    "C:/Users/Vladimir/Desktop/anomaly_detection_project/src/backend/ml_data_input/electricity_data_prepared.csv"
)
ex.prepare()
print(ex.get_data)
# ex.drop_column("gooooooal")
print(ex.get_data.head())

model = AnomalyDetector()
model.fit(ex.data, "электричество")
model.predict(ex.data, "электричество")
print(model.get_data)

df = ex.data
anomalies = df[df["anomaly"] == -1]

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
