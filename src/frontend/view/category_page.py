import flet as ft
import httpx
import os
import asyncio


class CategoryView:
    def __init__(self, app):
        self._app = app
        self._selected_resource = "электричество"
        self._text_color = self._app.update_text_colors()

        self._stars = self._app.gradient_noma(
            ft.Icon(ft.Icons.AUTO_AWESOME_SHARP, size=70)
        )

        self._choose = ft.CupertinoSlidingSegmentedButton(
            thumb_color=ft.Colors.INDIGO_400,
            on_change=self.change_resource,
            controls=[
                ft.Text("Электричество", font_family="sf", size=24),
                ft.Text("Вода", font_family="sf", size=24),
                ft.Text("Газ", font_family="sf", size=24),
            ],
            selected_index=0,
        )

        self._button = ft.ElevatedButton(
            text="Выберите CSV-файл",
            on_click=lambda e: self._app._file_picker.pick_files(
                allowed_extensions=["csv"]
            ),
            color=self._text_color,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=24, font_family="sf"),
                padding=20,
            ),
        )

        self._status_text = ft.Text("", font_family="sf", size=18)

        self._goto_analysis_button = ft.ElevatedButton(
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

        self._app._file_picker.on_result = lambda e: asyncio.run(self.upload_file(e))

    def change_resource(self, e: ft.ControlEvent) -> None:
        index = self._choose.selected_index
        self._selected_resource = ["электричество", "вода", "газ"][index]

    async def upload_file(self, e: ft.FilePickerResultEvent) -> None:
        if not e.files:
            self._status_text.value = "Файл не выбран"
            self._status_text.color = "red"
            self._goto_analysis_button.visible = False
            self._update_controls()
            return

        file_path = e.files[0].path
        self._status_text.value = "\nЗагрузка..."
        self._status_text.color = "blue"
        self._goto_analysis_button.visible = False
        self._update_controls()

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "text/csv")}
                data = {"resource": self._selected_resource}

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "http://127.0.0.1:8000/upload", data=data, files=files
                    )

            if response.status_code == 200:
                self._status_text.value = "\nФайл успешно загружен и обработан!\n"
                self._status_text.color = "green"
                self._goto_analysis_button.visible = True
            else:
                self._status_text.value = f"\nОшибка: {response.text}"
                self._status_text.color = "red"
                self._goto_analysis_button.visible = False

        except Exception as ex:
            self._status_text.value = f"\nОшибка загрузки: {str(ex)}"
            self._status_text.color = "red"
            self._goto_analysis_button.visible = False

        self._update_controls()

    def goto_resource_page(self, e: ft.ControlEvent) -> None:
        route_map = {"электричество": "/electricity", "вода": "/water", "газ": "/gas"}
        self._app._page.go(route_map.get(self._selected_resource, "/home"))

    def _update_controls(self) -> None:
        self._status_text.update()
        self._goto_analysis_button.update()
        self._button.color = self._app.update_text_colors()
        self._button.update()
        self._app._page.update()

    def build(self) -> ft.View:
        self._text_color = self._app.update_text_colors()
        self._button.color = self._text_color
        self._status_text.color = self._status_text.color or self._text_color

        start = ft.Row(
            controls=[
                self._stars,
                ft.Text(
                    "\n\n\nДавайте начнём! Определитесь с категорией и загрузите данные",
                    size=40,
                    color=self._text_color,
                    font_family="sf",
                    text_align=ft.TextAlign.CENTER,
                ),
            ]
        )

        return ft.View(
            "/category",
            [
                self._app.app_bar(),
                ft.Column(
                    [
                        ft.Row([start], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([self._choose], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text("\n")]),
                        ft.Row([self._button], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row(
                            [self._status_text], alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [self._goto_analysis_button],
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
