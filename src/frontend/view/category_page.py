import flet as ft
import httpx
import os
import asyncio


class CategoryView:
    def __init__(self, app):
        self.app = app
        self.selected_resource = "электричество"
        self.text_color = self.app.update_text_colors()

        self.stars = self.app.gradient_noma(
            ft.Icon(ft.Icons.AUTO_AWESOME_SHARP, size=70)
        )

        self.choose = ft.CupertinoSlidingSegmentedButton(
            thumb_color=ft.Colors.INDIGO_400,
            on_change=self.change_resource,
            controls=[
                ft.Text("Электричество", font_family="sf", size=24),
                ft.Text("Вода", font_family="sf", size=24),
                ft.Text("Газ", font_family="sf", size=24),
            ],
            selected_index=0,
        )

        self.button = ft.ElevatedButton(
            text="Выберите CSV-файл",
            on_click=lambda e: self.app.file_picker.pick_files(
                allowed_extensions=["csv"]
            ),
            color=self.text_color,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=24, font_family="sf"),
                padding=20,
            ),
        )

        self.status_text = ft.Text("", font_family="sf", size=18)

        self.goto_analysis_button = ft.ElevatedButton(
            text="Перейти к анализу",
            visible=False,
            on_click=self.goto_resource_page,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.INDIGO_400,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=22, font_family="sf"),
                padding=20,
            ),
        )

        self.app.file_picker.on_result = lambda e: asyncio.run(self.upload_file(e))

    def change_resource(self, e: ft.ControlEvent):
        index = self.choose.selected_index
        self.selected_resource = ["электричество", "вода", "газ"][index]

    async def upload_file(self, e: ft.FilePickerResultEvent):
        if not e.files:
            self.status_text.value = "Файл не выбран"
            self.status_text.color = "red"
            self.goto_analysis_button.visible = False
            self._update_controls()
            return

        file_path = e.files[0].path
        self.status_text.value = "\nЗагрузка..."
        self.status_text.color = "blue"
        self.goto_analysis_button.visible = False
        self._update_controls()

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "text/csv")}
                data = {"resource": self.selected_resource}

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "http://127.0.0.1:8000/upload", data=data, files=files
                    )

            if response.status_code == 200:
                self.status_text.value = "\nФайл успешно загружен и обработан!\n"
                self.status_text.color = "green"
                self.goto_analysis_button.visible = True
            else:
                self.status_text.value = f"\nОшибка: {response.text}"
                self.status_text.color = "red"
                self.goto_analysis_button.visible = False

        except Exception as ex:
            self.status_text.value = f"\nОшибка загрузки: {str(ex)}"
            self.status_text.color = "red"
            self.goto_analysis_button.visible = False

        self._update_controls()

    def goto_resource_page(self, e: ft.ControlEvent):
        route_map = {"электричество": "/electricity", "вода": "/water", "газ": "/gas"}
        self.app.page.go(route_map.get(self.selected_resource, "/home"))

    def _update_controls(self):
        self.status_text.update()
        self.goto_analysis_button.update()
        self.button.color = self.app.update_text_colors()
        self.button.update()
        self.app.page.update()

    def build(self) -> ft.View:
        self.text_color = self.app.update_text_colors()
        self.button.color = self.text_color
        self.status_text.color = self.status_text.color or self.text_color
        
        start = ft.Row(
            controls=[
                self.stars,
                ft.Text(
                    "\n\n\nДавайте начнём! Определитесь с категорией и загрузите данные",
                    size=40,
                    color=self.text_color,
                    font_family="sf",
                    text_align=ft.TextAlign.CENTER,
                ),
            ]
        )

        return ft.View(
            "/category",
            [
                self.app.app_bar(),
                ft.Column(
                    [
                        ft.Row([start], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([self.choose], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("\n")]),
                        ft.Row([self.button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row(
                            [self.status_text], alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [self.goto_analysis_button],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            ],
        )
