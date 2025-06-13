import flet as ft


class WaterPage:
    def __init__(self, app):
        self.app = app
        self.text_color = self.app.update_text_colors()

    def container_for_data(self) -> ft.Container:
        return ft.Container(
            bgcolor="red", width=self.app.page.width, height=150, border_radius=20
        )

    def container_for_graphics(self) -> ft.Container:
        return ft.Container(
            bgcolor="blue", width=self.app.page.width, height=700, border_radius=20
        )

    def column_for_containers(self) -> ft.Column:
        return ft.Column(
            controls=[
                self.container_for_graphics(),
                self.container_for_data(),
            ],
            expand=True
        )

    def build(self) -> ft.View:
        return ft.View(
            "/water",
            controls=[self.app.app_bar(), self.column_for_containers()],
            scroll=ft.ScrollMode.AUTO,
        )
