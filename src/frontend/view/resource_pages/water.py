import flet as ft
import asyncio
import pandas as pd
import httpx
import sys
import os
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from backend.utils.plot_utils import generate_water_plot


class WaterPage:
    def __init__(self, app):
        self.app = app
        self.text_color = self.app.update_text_colors()
        self.theme = (
            "dark" if self.app.page.theme_mode == ft.ThemeMode.DARK else "light"
        )
        self.graph_path = ""
        self.anomalies_list = []

    async def load_data(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://127.0.0.1:8000/measurements?resource=water"
                )
                data = response.json()

            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df["is_anomaly"] = df["is_anomaly"].astype(bool)
            self.graph_path = generate_water_plot(df, theme=self.theme)
            self.anomalies_list = df[df["is_anomaly"] == True][
                ["datetime", "value"]
            ].to_dict(orient="records")

        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке или обработке данных: {e}")

    def container_for_graphics(self) -> ft.Container:
        if not self.graph_path or not os.path.exists(self.graph_path):
            return ft.Container(
                content=ft.Text("График не найден", color="red", size=20),
                border_radius=20,
                padding=20,
            )

        with open(self.graph_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        return ft.Container(
            content=ft.Image(
                src_base64=encoded,
                width=self.app.page.width,
                height=600,
                fit=ft.ImageFit.CONTAIN,
            ),
            border_radius=20,
            padding=10,
        )

    def container_for_anomalies(self) -> ft.Container:
        items = []
        for a in self.anomalies_list:
            items.append(
                ft.Text(
                    f"{a['datetime']} — {a['value']} ед.",
                    color="red",
                    size=16,
                    font_family="sf",
                )
            )

        return ft.Container(
            content=ft.ListView(
                controls=items,
                expand=True,
                spacing=5,
                padding=10,
            ),
            bgcolor="white10" if self.theme == "dark" else "black12",
            height=300,
            border_radius=10,
            expand=True,
        )

    async def build_async(self):
        await self.load_data()
        return ft.View(
            "/water",
            controls=[
                self.app.app_bar(),
                ft.Column(
                    controls=[
                        self.container_for_graphics(),
                        ft.Text(
                            "Выявленные аномалии",
                            size=22,
                            weight="bold",
                            color=self.text_color,
                            font_family="sf",
                        ),
                        self.container_for_anomalies(),
                    ],
                    spacing=30,
                    expand=True,
                    width=self.app.page.width,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
