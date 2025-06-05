import flet as ft


class CategoryView:
    def __init__(self, app):
        self.app = app
        self.stars = ft.ShaderMask(
            content=ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, size=70),
            blend_mode=ft.BlendMode.SRC_IN,
            shader=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[
                    ft.Colors.BLUE_400,
                    ft.Colors.INDIGO_500,
                    ft.Colors.PURPLE_400,
                    ft.Colors.DEEP_PURPLE_300,
                ],
                stops=[0.0, 0.4, 0.7, 1.0],
                tile_mode=ft.GradientTileMode.MIRROR,
            ),
        )

    def build(self) -> ft.View:
        textclr = self.app.update_text_colors()

        start = ft.Row(
            controls=[
                self.stars,
                ft.Text(
                    "\n\n\nДавайте начнём! Определитесь с категорией и загрузите данные",
                    size=40,
                    color=textclr,
                    font_family="sf",
                    text_align=ft.TextAlign.CENTER,
                )
            ]
        )

        choose = ft.CupertinoSlidingSegmentedButton(
            thumb_color=ft.Colors.INDIGO_400,
            controls=[
                ft.Text("Электричество", font_family="sf", color=textclr, size=30),
                ft.Text("Вода", font_family="sf", color=textclr, size=30),
                ft.Text("Газ", font_family="sf", color=textclr, size=30),
            ],
        )

        button = ft.ElevatedButton(
            text="Выберите файл",
            on_click=lambda e: self.app.file_picker.pick_files(),
            color=textclr,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=30, font_family="sf", color=textclr),
                padding=20,
            ),
        )

        return ft.View(
            "/category",
            [
                self.app.app_bar(),
                ft.Column(
                    [
                        ft.Row([start], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([choose], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("\n")], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("\n")], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ],
            padding=0,
        )
