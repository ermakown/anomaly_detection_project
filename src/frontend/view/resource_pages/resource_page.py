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
        self._app = app
        self._resource = resource
        self._label = label
        self._title = title
        self._icon = icon
        self._main_color = main_color
        self._anomaly_color = anomaly_color

        self._theme = (
            "dark" if self._app._page.theme_mode == ft.ThemeMode.DARK else "light"
        )
        self._text_color = self._app.update_text_colors()
        self._graph_path = ""
        self._anomalies_list = []
        self._max_anomaly_value = 0
        self._min_anomaly_value = 100000
        self._max_anomaly_date = ""
        self._min_anomaly_date = ""

    async def load_data(self) -> None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://127.0.0.1:8000/measurements?resource={self._resource}"
                )
                data = response.json()

            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df["is_anomaly"] = df["is_anomaly"].astype(bool)

            if self._resource == "вода":
                if self._theme == "dark":
                    main_color = "royalblue"
                    anomaly_color = "cornflowerblue"
                    axis_color = "white"
                else:
                    main_color = "cornflowerblue"
                    anomaly_color = "royalblue"
                    axis_color = "black"
            elif self._resource == "газ":
                if self._theme == "dark":
                    main_color = "darkred"
                    anomaly_color = "firebrick"
                    axis_color = "white"
                else:
                    main_color = "firebrick"
                    anomaly_color = "darkred"
                    axis_color = "black"
            elif self._resource == "электричество":
                if self._theme == "dark":
                    main_color = "darkgoldenrod"
                    anomaly_color = "goldenrod"
                    axis_color = "white"
                else:
                    main_color = "goldenrod"
                    anomaly_color = "darkgoldenrod"
                    axis_color = "black"
            else:
                main_color = self._main_color
                anomaly_color = self._anomaly_color
                axis_color = "white" if self._theme == "dark" else "black"

            self._graph_path = generate_resource_plot(
                df,
                resource=self._resource,
                theme=self._theme,
                main_color=main_color,
                anomaly_color=anomaly_color,
                axis_color=axis_color,
            )

            self._anomalies_list = df[df["is_anomaly"] == True][
                ["datetime", "value"]
            ].to_dict(orient="records")

            for i in self._anomalies_list:
                if i["value"] > self._max_anomaly_value:
                    self._max_anomaly_value = i["value"]
                    self._max_anomaly_date = i["datetime"]
                if i["value"] < self._min_anomaly_value:
                    self._min_anomaly_value = i["value"]
                    self._min_anomaly_date = i["datetime"]

        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке данных: {e}")

    def recomendations(self) -> ft.Text:
        count = len(self._anomalies_list)
        if count <= 20:
            return ft.Text(
                f"Уровень потребления {self._label} в пределах нормы. Продолжайте в том же духе!",
                font_family="sf",
                color=self._text_color,
                size=14,
            )
        elif 20 < count <= 50:
            return ft.Text(
                f"Потребление {self._label} превышает нормы. Попробуйте снизить расход.",
                font_family="sf",
                color=self._text_color,
                size=14,
            )
        else:
            return ft.Text(
                "Критический уровень аномалий!\n"
                f"Усерднее контролируйте потребление, а также проверьте систему {self._label} "
                "и, при обнаружении неисправностей, "
                "как можно скорее устраните их.",
                font_family="sf",
                color=self._text_color,
                size=14,
            )

    def container_for_graphics(self) -> ft.Container:
        if not self._graph_path or not os.path.exists(self._graph_path):
            return ft.Container(
                content=ft.Text("График не найден", color="red"), padding=20
            )

        with open(self._graph_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        return ft.Container(
            content=ft.Image(
                src_base64=encoded,
                width=self._app._page.width,
                height=600,
                fit=ft.ImageFit.CONTAIN,
            ),
            padding=10,
            border_radius=20,
            expand=True,
        )

    def container_for_anomalies(self) -> ft.Container:
        columns = [
            ft.DataColumn(ft.Text("Дата", font_family="sf", color=self._text_color)),
            ft.DataColumn(ft.Text("Время", font_family="sf", color=self._text_color)),
            ft.DataColumn(
                ft.Text("Показатель", font_family="sf", color=self._text_color)
            ),
        ]
        rows = []
        for i in self._anomalies_list:
            dt = pd.to_datetime(i["datetime"])
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                dt.strftime("%d.%m.%Y"),
                                font_family="sf",
                                color=self._text_color,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                dt.strftime("%H:%M"),
                                font_family="sf",
                                color=self._text_color,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(i["value"]),
                                font_family="sf",
                                color=self._main_color,
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
                            "Всего аномалий:", color=self._text_color, font_family="sf"
                        ),
                        ft.Text(
                            str(len(self._anomalies_list)),
                            color=self._main_color,
                            font_family="sf",
                        ),
                    ]
                ),
                ft.Text(),
                ft.Text(
                    f"Макс: {self._max_anomaly_value} | {self._max_anomaly_date}",
                    font_family="sf",
                    color=self._text_color,
                ),
                ft.Text(
                    f"Мин: {self._min_anomaly_value} | {self._min_anomaly_date}",
                    font_family="sf",
                    color=self._text_color,
                ),
                ft.Text(),
                ft.Text("Рекомендации:", font_family="sf", color=self._text_color),
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
                        bgcolor="black10" if self._theme == "dark" else "white10",
                        border=ft.border.all(3, color=self._main_color),
                    ),
                    ft.Container(
                        content=stats,
                        expand=True,
                        height=350,
                        padding=10,
                        border_radius=10,
                        border=ft.border.all(3, color=self._main_color),
                        bgcolor="black10" if self._theme == "dark" else "white10",
                    ),
                ],
                spacing=20,
            ),
            padding=10,
        )

    async def build_async(self) -> ft.View:
        await self.load_data()
        return ft.View(
            f"/{self._resource}",
            controls=[
                self._app.app_bar(),
                ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Icon(self._icon, size=40, color=self._main_color),
                                ft.Text(
                                    self._title,
                                    size=40,
                                    color=self._text_color,
                                    weight="bold",
                                ),
                            ],
                            alignment="center",
                        ),
                        self.container_for_graphics(),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Выявленные аномалии",
                                    size=22,
                                    weight="bold",
                                    color=self._text_color,
                                    font_family="sf",
                                ),
                                ft.Icon(
                                    ft.Icons.ARROW_DOWNWARD_ROUNDED,
                                    size=22,
                                    color=self._text_color,
                                ),
                            ],
                            alignment="center",
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
