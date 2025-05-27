import flet as ft


class MainView:
    def __init__(self, app) -> ft.View:
        self.app = app

    def build(self):
        textclr, logo_src, sidebar_color = self.app.update_colors()

        logo = ft.Image(src=logo_src, width=300, height=300)

        title = ft.Text(
            "Добро пожаловать в",
            font_family="jura",
            size=70,
            color=textclr,
            weight=ft.FontWeight.BOLD,
        )
        name = ft.Text(
            "Нома",
            font_family="jura",
            size=60,
            color=ft.Colors.BLUE_400,
            weight=ft.FontWeight.BOLD,
        )
        desc = ft.Text(
            "Удобный инструмент контроля потребления ресурсов",
            size=25,
            color=textclr,
            font_family="jura",
            text_align=ft.TextAlign.CENTER,
        )

        button_start = ft.ElevatedButton(
            text="Начать",
            on_click=lambda e: self.app.page.go(
                "/home", ft.PageTransitionTheme.PREDICTIVE
            ),
            color=textclr,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=25, font_family="jura", color=textclr),
                padding=20,
            ),
        )

        return ft.View(
            "/",
            [
                ft.Column(
                    [
                        ft.Row([title], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([logo], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([name], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([desc], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("\n")], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([button_start], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                )
            ],
            padding=20,
        )
