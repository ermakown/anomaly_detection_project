import flet as ft


class CategoryView:
    def __init__(self, app):
        self.app = app

    def build(self) -> ft.View:
        textclr, logo_src, sidebar_color = self.app.update_colors()

        start = ft.Text(
            "\n\n\nНу что ж, приступим? Определитесь с категорией и загрузите данные",
            size=40,
            color=textclr,
            font_family="jura",
            text_align=ft.TextAlign.CENTER,
        )

        choose = ft.CupertinoSlidingSegmentedButton(
            thumb_color=ft.Colors.BLUE_400,
            controls=[
                ft.Text("Электричество", font_family="jura", color=textclr, size=30),
                ft.Text("Вода", font_family="jura", color=textclr, size=30),
                ft.Text("Газ", font_family="jura", color=textclr, size=30),
            ],
        )

        button = ft.ElevatedButton(
            text="Выберите файл",
            on_click=lambda e: self.app.file_picker.pick_files(),
            color=textclr,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=30, font_family="jura", color=textclr),
                padding=20,
            ),
        )

        button_back = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_ROUNDED,
            on_click=lambda e: self.app.page.go("/", ft.PageTransitionTheme.PREDICTIVE),
            icon_color=textclr,
        )

        button_first_page = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
            on_click=lambda e: self.app.page.go(
                "/home", ft.PageTransitionTheme.PREDICTIVE
            ),
            icon_color=textclr,
        )

        return ft.View(
            "/category",
            [
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
                    actions=[self.app.theme_button],
                ),
                ft.Column(
                    [
                        ft.Row([start], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([choose], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("\n")], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("\n")], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([button_back], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row(
                            [button_first_page], alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ],
            padding=0,
        )
