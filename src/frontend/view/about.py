import flet as ft


class About:
    def __init__(self, app):
        self._app = app
        self._text_color = self._app.update_text_colors()
        self._image_color = self._app.update_logo_colors()
        self._name = self._app.gradient_noma(
            ft.Text("Noma", font_family="sf", size=100)
        )

    def image_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Image(src=self._image_color, height=500, width=500),
            alignment=ft.alignment.center_left,
            expand=True,
            padding=ft.Padding(100, 50, 0, 0),
            border_radius=10,
        )

    def info_text(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    self._name,
                    ft.Text(
                        "— это удобный инструмент для анализа потребления\n"
                        "воды, электроэнергии и газа. Загружайте данные, находите\n"
                        "аномалии и получайте рекомендации по оптимизации затрат.\n\n"
                        "Noma использует алгоритмы машинного обучения для обнаружения "
                        "необычных пиков потребления ресурсов. Система наглядно представляет "
                        "информацию, выделяет аномалии и помогает отслеживать рациональность "
                        "использования газа, воды и электроэнергии в доме.\n\n"
                        "Интерфейс прост и интуитивен — Вы сразу можете приступить к работе: "
                        "выбрать категорию, импортировать CSV-файл и переходить к анализу.\n\n"
                        "Своевременное обнаружение аномалий может предотвратить утечки, "
                        "улучшить бюджет и сделать Ваш дом энергоэффективным.",
                        size=20,
                        font_family="sf",
                        color=self._text_color,
                    ),
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=ft.Padding(0, 50, 100, 0),
            border_radius=10,
        )

    def build(self) -> ft.View:
        return ft.View(
            "/about",
            controls=[
                self._app.app_bar(),
                ft.Row(controls=[self.image_container(), self.info_text()]),
            ],
        )
