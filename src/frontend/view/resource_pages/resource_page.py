import flet as ft
import asyncio
import pandas as pd
import httpx
import os
import base64
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from backend.utils.plot_utils import generate_resource_plot


class ResourcePage:
    def __init__(
        self,
        app,
        resource: str,
        label: str,
        title: str,
        icon: ft.Icon,
        main_color: str,
        anomaly_color: str,
    ):
        self.app = app
        self.resource = resource
        self.label = label
        self.title = title
        self.icon = icon
        self.main_color = main_color
        self.anomaly_color = anomaly_color

        self.theme = (
            "dark" if self.app.page.theme_mode == ft.ThemeMode.DARK else "light"
        )
        self.text_color = self.app.update_text_colors()
        self.graph_path = ""
        self.anomalies_list = []
        self.max_anomaly_value = 0
        self.min_anomaly_value = 1e6
        self.max_anomaly_date = ""
        self.min_anomaly_date = ""

    async def load_data(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://127.0.0.1:8000/measurements?resource={self.resource}"
                )
                data = response.json()

            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df["is_anomaly"] = df["is_anomaly"].astype(bool)

            if self.resource == "вода":
                if self.theme == "dark":
                    main_color = "royalblue"
                    anomaly_color = "cornflowerblue"
                    axis_color = "white"
                else:
                    main_color = "cornflowerblue"
                    anomaly_color = "royalblue"
                    axis_color = "black"
            elif self.resource == "газ":
                if self.theme == "dark":
                    main_color = "darkred"
                    anomaly_color = "firebrick"
                    axis_color = "white"
                else:
                    main_color = "firebrick"
                    anomaly_color = "darkred"
                    axis_color = "black"
            elif self.resource == "электричество":
                if self.theme == "dark":
                    main_color = "darkgoldenrod"
                    anomaly_color = "goldenrod"
                    axis_color = "white"
                else:
                    main_color = "goldenrod"
                    anomaly_color = "darkgoldenrod"
                    axis_color = "black"
            else:
                main_color = self.main_color
                anomaly_color = self.anomaly_color
                axis_color = "white" if self.theme == "dark" else "black"

            self.graph_path = generate_resource_plot(
                df,
                resource=self.resource,
                theme=self.theme,
                main_color=main_color,
                anomaly_color=anomaly_color,
                axis_color=axis_color,
            )

            self.anomalies_list = df[df["is_anomaly"] == True][
                ["datetime", "value"]
            ].to_dict(orient="records")

            for i in self.anomalies_list:
                if i["value"] > self.max_anomaly_value:
                    self.max_anomaly_value = i["value"]
                    self.max_anomaly_date = i["datetime"]
                if i["value"] < self.min_anomaly_value:
                    self.min_anomaly_value = i["value"]
                    self.min_anomaly_date = i["datetime"]

        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке данных: {e}")

    def recomendations(self) -> ft.Text:
        count = len(self.anomalies_list)
        if count <= 20:
            return ft.Text(
                f"Уровень потребления {self.label} в пределах нормы. Продолжайте в том же духе!",
                font_family="sf",
                color=self.text_color,
                size=14,
            )
        elif 20 < count <= 50:
            return ft.Text(
                f"Потребление {self.label} превышает нормы. Попробуйте снизить расход.",
                font_family="sf",
                color=self.text_color,
                size=14,
            )
        else:
            return ft.Text(
                f"Критический уровень аномалий. Проверьте систему {self.label} и устраните неисправности.",
                font_family="sf",
                color=self.text_color,
                size=14,
            )

    def container_for_graphics(self) -> ft.Container:
        if not self.graph_path or not os.path.exists(self.graph_path):
            return ft.Container(
                content=ft.Text("График не найден", color="red"), padding=20
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
            padding=10,
            border_radius=20,
            expand=True,
        )

    def container_for_anomalies(self) -> ft.Container:
        columns = [
            ft.DataColumn(ft.Text("Дата", font_family="sf", color=self.text_color)),
            ft.DataColumn(ft.Text("Время", font_family="sf", color=self.text_color)),
            ft.DataColumn(
                ft.Text("Показатель", font_family="sf", color=self.text_color)
            ),
        ]
        rows = []
        for i in self.anomalies_list:
            dt = pd.to_datetime(i["datetime"])
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                dt.strftime("%d.%m.%Y"),
                                font_family="sf",
                                color=self.text_color,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                dt.strftime("%H:%M"),
                                font_family="sf",
                                color=self.text_color,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(i["value"]), font_family="sf", color=self.main_color
                            )
                        ),
                    ]
                )
            )

        table = ft.DataTable(
            columns=columns,
            rows=rows,
            heading_text_style=ft.TextStyle(weight="bold"),
            heading_row_color=ft.Colors.BLACK12,
            border_radius=10,
            column_spacing=20,
            horizontal_margin=10,
            divider_thickness=1,
        )

        stats = ft.ListView(
            controls=[
                ft.Row(
                    [
                        ft.Text(
                            "Всего аномалий:", color=self.text_color, font_family="sf"
                        ),
                        ft.Text(
                            str(len(self.anomalies_list)),
                            color=self.main_color,
                            font_family="sf",
                        ),
                    ]
                ),
                ft.Text(),
                ft.Text(
                    f"Макс: {self.max_anomaly_value} | {self.max_anomaly_date}",
                    font_family="sf",
                    color=self.text_color,
                ),
                ft.Text(
                    f"Мин: {self.min_anomaly_value} | {self.min_anomaly_date}",
                    font_family="sf",
                    color=self.text_color,
                ),
                ft.Text(),
                ft.Text("Рекомендации:", font_family="sf", color=self.text_color),
                self.recomendations(),
            ],
            spacing=10,
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.ListView([table]),
                        expand=True,
                        height=350,
                        border_radius=10,
                        bgcolor="black10" if self.theme == "dark" else "white10",
                        border=ft.border.all(3, color=self.main_color),
                    ),
                    ft.Container(
                        content=stats,
                        expand=True,
                        height=350,
                        padding=10,
                        border_radius=10,
                        border=ft.border.all(3, color=self.main_color),
                        bgcolor="black10" if self.theme == "dark" else "white10",
                    ),
                ],
                spacing=20,
            ),
            padding=10,
        )

    async def build_async(self):
        await self.load_data()
        return ft.View(
            f"/{self.resource}",
            controls=[
                self.app.app_bar(),
                ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Icon(self.icon, size=40, color=self.main_color),
                                ft.Text(
                                    self.title,
                                    size=40,
                                    color=self.text_color,
                                    weight="bold",
                                ),
                            ],
                            alignment="center",
                        ),
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
                    horizontal_alignment="center",
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            padding=20,
        )
