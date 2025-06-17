import flet as ft


class HomePageView:
    def __init__(self, app):
        self.app = app
        self.logo = self.app.gradient_noma(ft.Text("Noma", size=130, font_family="sf"))
        self.hello_text = ft.Text(
            "Сделайте свою жизнь\nпонятнее",
            font_family="sf",
            size=35,
            weight=ft.FontWeight.BOLD,
        )
        self.description = ft.Text(
            "Самостоятельно анализируйте потребление\nресурсов в Вашем доме",
            font_family="sf",
            size=18,
        )

        self.text_color = self.app.update_text_colors()

    def page_logo(self) -> ft.Container:
        return ft.Container(
            bgcolor=None,
            width=650,
            border_radius=10,
            padding=ft.Padding(0, 50, 0, 0),
            content=ft.Row(
                controls=[
                    ft.Container(width=100),
                    ft.Column(
                        controls=[
                            self.logo,
                            self.hello_text,
                            self.description,
                            ft.Row(controls=[ft.Text("\n")]),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                        tight=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                ]
            ),
        )

    def icons(self) -> ft.Container:
        return ft.Container(
            bgcolor=None,
            width=450,
            alignment=ft.alignment.top_center,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.WATER_DROP_ROUNDED,
                                        size=100,
                                        color=self.text_color,
                                    ),
                                    ft.Icon(
                                        ft.Icons.ELECTRICAL_SERVICES_ROUNDED,
                                        size=400,
                                        color=self.text_color,
                                    ),
                                    ft.Icon(
                                        ft.Icons.GAS_METER_ROUNDED,
                                        size=180,
                                        color=self.text_color,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=0,
                    ),
                    ft.Row(
                        controls=[
                            self.app.gradient_noma(
                                ft.Icon(
                                    ft.Icons.INSIGHTS_ROUNDED,
                                    size=140,
                                    color=self.text_color,
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(0, 0, 0, 0),
        )

    def hello(self) -> ft.Row:
        return ft.Row(controls=[self.page_logo(), self.icons()], expand=True, spacing=0)

    def build(self) -> ft.View:

        return ft.View(
            "/home",
            controls=[
                self.app.app_bar(),
                self.hello()
            ],
        )
