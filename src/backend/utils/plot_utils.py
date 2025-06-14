import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os
from matplotlib.dates import DateFormatter


def generate_water_plot(df: pd.DataFrame, resource: str, theme: str = "light") -> str:
    if theme == "dark":
        plt.style.use("dark_background")
        line_color = "royalblue"
        anomaly_color = "cornflowerblue"
        axis_color = "white"
    else:
        plt.style.use("default")
        line_color = "cornflowerblue"
        anomaly_color = "royalblue"
        axis_color = "black"

    fig, ax = plt.subplots(figsize=(13, 6))

    ax.plot(df["datetime"], df["value"], label="Потребление", color=line_color)
    anomalies = df[df["is_anomaly"] == True]
    ax.scatter(
        anomalies["datetime"],
        anomalies["value"],
        color=anomaly_color,
        label="Аномалии",
        zorder=5,
    )

    ax.set_title(f"Потребление ресурса\n", color=axis_color)
    ax.set_xlabel("\nДата и время", color=axis_color)
    ax.set_ylabel("Объём потребления\n", color=axis_color)
    ax.tick_params(axis="x", colors=axis_color)
    ax.tick_params(axis="y", colors=axis_color)
    ax.spines["bottom"].set_color(axis_color)
    ax.spines["top"].set_color(axis_color)
    ax.spines["left"].set_color(axis_color)
    ax.spines["right"].set_color(axis_color)
    ax.legend()

    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))

    temp_path = os.path.join(tempfile.gettempdir(), f"{resource}_graph_{theme}.png")
    plt.tight_layout()
    plt.savefig(temp_path, transparent=True)
    plt.close(fig)

    return temp_path
