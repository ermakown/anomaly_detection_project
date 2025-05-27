import flet as ft


class HomePageView:
    def __init__(self, app):
        self.app = app

    def build(self) -> ft.View:
        textclr, logo_src, sidebar_color = self.app.update_colors()

        button_back = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,
            on_click=lambda e: self.app.page.go(
                "/category", ft.PageTransitionTheme.PREDICTIVE
            ),
            icon_color=textclr,
        )

        sidebar = ft.Container(
            width=80,
            bgcolor=sidebar_color,
            padding=10,
            border_radius=20,
            expand=False,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.HOME_ROUNDED,
                        icon_color=textclr,
                        icon_size=25,
                        tooltip="Главная",
                        style=ft.ButtonStyle(overlay_color=sidebar_color),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DOWNLOAD_ROUNDED,
                        icon_color=textclr,
                        icon_size=25,
                        tooltip="Загрузка данных",
                        style=ft.ButtonStyle(overlay_color=sidebar_color),
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.LIGHTBULB_ROUNDED,
                        icon_color=ft.Colors.ORANGE_400,
                        icon_size=45,
                        tooltip="Электричество",
                        style=ft.ButtonStyle(overlay_color=sidebar_color),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.WATER_DROP_ROUNDED,
                        icon_color=ft.Colors.BLUE_400,
                        icon_size=45,
                        tooltip="Вода",
                        style=ft.ButtonStyle(overlay_color=sidebar_color),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.GAS_METER_ROUNDED,
                        icon_color=ft.Colors.RED_400,
                        icon_size=45,
                        tooltip="Газ",
                        style=ft.ButtonStyle(overlay_color=sidebar_color),
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DESCRIPTION_ROUNDED,
                        icon_color=textclr,
                        icon_size=25,
                        tooltip="Инфо",
                        style=ft.ButtonStyle(overlay_color=sidebar_color),
                    ),
                    ft.IconButton(
                        icon=self.app.get_theme_icon(),
                        on_click=self.app.toggle_theme,
                        icon_color=textclr,
                        icon_size=25,
                        tooltip="Тема",
                        style=ft.ButtonStyle(overlay_color=sidebar_color),
                    ),
                ],
            ),
        )

        return ft.View(
            "/first_page",
            controls=[
                ft.AppBar(
                    center_title=True,
                    title=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            ft.Image(src=logo_src, width=40, height=40),
                            ft.Container(width=10),
                            ft.Text("Нома", color=textclr, font_family="jura"),
                        ],
                    ),
                ),
                ft.Row(
                    [
                        sidebar,
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        controls=[button_back],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    expand=True,
                                    bgcolor="blue",
                                    border_radius=20,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                            spacing=0,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        )
