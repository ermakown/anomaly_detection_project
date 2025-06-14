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
        self.anomalies_list = list()
        self.max_anomaly_date: None | str = None
        self.max_anomaly_value = 0.0
        self.min_anomaly_date: None | str = None
        self.min_anomaly_value = 1000.0

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
            self.graph_path = generate_water_plot(df, "вода", theme=self.theme)
            self.anomalies_list = df[df["is_anomaly"] == True][
                ["datetime", "value"]
            ].to_dict(orient="records")

        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке или обработке данных: {e}")

    def recomendations(self) -> ft.Text:
        if len(self.anomalies_list) <= 20:
            return ft.Text(
                "Уровень потребления воды находится в пределах нормы, значительные отклонения наблюдаются редко. Рекомендуем придерживаться текущего режима потребления",
                font_family="sf",
                color=self.text_color,
                size=14,
            )
        elif 20 > len(self.anomalies_list) <= 50:
            return ft.Text(
                "Уровень потребления воды превышает нормативные показатели, при этом частые аномалии указывают на нерациональное использование ресурсов. Рекомендуем принять меры по сокращению расхода, в частности:\n\n1)отключать воду в моменты, когда она не требуется (например, во время чистки зубов или нанесения моющего средства при мытье посуды);\n\n2)усилить контроль за потреблением для своевременного выявления и устранения перерасхода.",
                font_family="sf",
                color=self.text_color,
                size=14,
            )
        else:
            return ft.Text(
                "Уровень потребления воды значительно превышает установленные нормативы, при этом систематические аномалии указывают на возможные неисправности или нерациональное использование ресурсов.\n\nРекомендуем:\n\n1)Усилить контроль за водопотреблением для выявления и устранения причин перерасхода.\n2)Провести диагностику водопроводной системы на предмет утечек, повреждений труб или неисправности сантехнического оборудования.\n3)Оптимизировать расход воды за счет соблюдения следующих мер:\n\t\ta)отключать воду при чистке зубов, нанесении моющих средств;\n\t\tb)использовать экономичные режимы бытовой техники;\n\t\tc)оперативно устранять протечки.\n\nСвоевременное принятие мер позволит снизить затраты и избежать дальнейшего перерасхода.",
                font_family="sf",
                color=self.text_color,
                size=14,
            )

    def container_for_graphics(self) -> ft.Container:
        if not self.graph_path or not os.path.exists(self.graph_path):
            return ft.Container(
                content=ft.Text("График не найден", color="red", size=20),
                border_radius=20,
                padding=20,
                alignment="start",
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
            date = dt.strftime("%d.%m.%Y")
            time = dt.strftime("%H:%M")
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(date, color=self.text_color, font_family="sf")
                        ),
                        ft.DataCell(
                            ft.Text(time, color=self.text_color, font_family="sf")
                        ),
                        ft.DataCell(
                            ft.Text(str(i["value"]), color="blue", font_family="sf")
                        ),
                    ]
                )
            )
            if i["value"] > self.max_anomaly_value:
                self.max_anomaly_value = i["value"]
                self.max_anomaly_date = i["datetime"]
            if i["value"] < self.min_anomaly_value:
                self.min_anomaly_value = i["value"]
                self.min_anomaly_date = i["datetime"]

        scrollable_table = ft.Container(
            content=ft.Container(
                content=ft.ListView(
                    controls=[
                        ft.DataTable(
                            columns=columns,
                            rows=rows,
                            border_radius=10,
                            heading_row_color=ft.Colors.BLACK12,
                            heading_text_style=ft.TextStyle(weight="bold"),
                            divider_thickness=1,
                            column_spacing=20,
                            horizontal_margin=10,
                        )
                    ],
                    auto_scroll=False,
                ),
                expand=True,
            ),
            height=350,
            padding=10,
            bgcolor=("white10" if self.theme == "white" else "black10"),
            border_radius=10,
            border=ft.border.all(3, color="blue"),
            expand=True,
        )

        right_block = ft.Container(
            content=ft.ListView(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Всего аномалий:",
                                color=self.text_color,
                                font_family="sf"
                            ),
                            ft.Text(
                                str(len(self.anomalies_list)), color="blue", font_family="sf"
                            ),
                        ]
                    ),
                    ft.Text(),
                    ft.Text(
                        f"Минимальный показатель аномалий:  {self.min_anomaly_value}    |   Дата:   {self.min_anomaly_date}",
                        font_family="sf",
                        color=self.text_color,
                    ),
                    ft.Text(
                        f"Максимальный показатель аномалий:  {self.max_anomaly_value}    |   Дата:   {self.max_anomaly_date}",
                        font_family="sf",
                        color=self.text_color,
                    ),
                    ft.Text(),
                    ft.Text("Рекомендации:", color=self.text_color, font_family="sf"),
                    self.recomendations(),
                ],
                expand=True,
                auto_scroll=False,
                spacing=10,
            ),
            padding=10,
            expand=True,
            border=ft.border.all(3, color="blue"),
            border_radius=10,
            height=350,
            bgcolor=("white10" if self.theme == "white" else "black10"),
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(controls=[scrollable_table, right_block], spacing=20),
                ],
                spacing=10,
            ),
            padding=10,
        )

    async def build_async(self):
        await self.load_data()
        return ft.View(
            "/water",
            controls=[
                self.app.app_bar(),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.WATER_DROP_ROUNDED, size=40, color="blue"
                                ),
                                ft.Text(
                                    "Показатели воды",
                                    color=self.text_color,
                                    size=40,
                                    weight="bold"
                                ),
                            ],
                            alignment="center"
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
                    width=self.app.page.width,
                    horizontal_alignment="center",
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            padding=20,
        )
