import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os
from matplotlib.dates import DateFormatter


def generate_resource_plot(
    df: pd.DataFrame,
    resource: str,
    theme: str = "light",
    main_color: str = "blue",
    anomaly_color: str = "violet",
    axis_color: str = "black",
) -> str:
    if theme == "dark":
        plt.style.use("dark_background")
    else:
        plt.style.use("default")

    fig, ax = plt.subplots(figsize=(13, 6))

    ax.plot(df["datetime"], df["value"], label="Потребление", color=main_color)

    anomalies = df[df["is_anomaly"] == True]
    ax.scatter(
        anomalies["datetime"],
        anomalies["value"],
        color=anomaly_color,
        label="Аномалии",
        zorder=5,
    )

    ax.set_title(f"Потребление ресурса — {resource}", color=axis_color, fontsize=14)
    ax.set_xlabel("Дата и время", color=axis_color)
    ax.set_ylabel("Объём потребления", color=axis_color)

    ax.tick_params(axis="x", colors=axis_color)
    ax.tick_params(axis="y", colors=axis_color)
    for spine in ax.spines.values():
        spine.set_color(axis_color)

    ax.legend()
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.tight_layout()

    path = os.path.join(tempfile.gettempdir(), f"{resource}_graph_{theme}.png")
    plt.savefig(path, transparent=True)
    plt.close(fig)
    return path
