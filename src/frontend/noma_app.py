from typing import Union
import flet as ft
import asyncio
from view.category_page import CategoryView
from view.home import HomePageView
from view.resource_pages.resource_page import ResourcePage
from view.about import About


class NomaApp:
    def __init__(self, page: ft.Page):
        self._page = page
        self._page.title = "Noma"
        self._page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self._page.padding = 20
        self._page.scroll = ft.ScrollMode.AUTO
        self._page.fonts = {"jura": "/fonts/Jura.ttf", "sf": "/fonts/System Font.ttf"}
        self._page.theme_mode = self.detect_theme_mode()
        self._text_color: None | str = None
        self._logo_src: None | str = None

        self._theme_button = ft.IconButton(
            icon=self.get_theme_icon(), on_click=self.toggle_theme
        )

        self._file_picker = ft.FilePicker()
        self._page.overlay.append(self._file_picker)

        self._page.on_route_change = self.route_change
        self._views = {
            "/category": CategoryView,
            "/home": HomePageView,
            "/about": About
        }

        self._app_bar_style = ft.ButtonStyle(
            text_style=ft.TextStyle(color=self._text_color, size=18, font_family="sf")
        )

    def detect_theme_mode(self) -> ft.ThemeMode:

        return (
            ft.ThemeMode.DARK
            if self._page.platform_brightness == ft.Brightness.DARK
            else ft.ThemeMode.LIGHT
        )

    def get_theme_icon(self) -> ft.Icons:
        return (
            ft.Icons.LIGHT_MODE_ROUNDED
            if self._page.theme_mode == ft.ThemeMode.DARK
            else ft.Icons.DARK_MODE_ROUNDED
        )

    def toggle_theme(self, e: ft.ControlEvent) -> None:

        self._page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self._page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        self._theme_button.icon = self.get_theme_icon()
        self.route_change(None)

    def gradient_noma(self, target: Union[ft.Text, ft.Icon]) -> ft.ShaderMask:
        return ft.ShaderMask(
            content=target,
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

    def update_logo_colors(self) -> str:
        if self._page.theme is None:
            self._page.theme = ft.Theme()

        if self._page.theme_mode == ft.ThemeMode.DARK:
            self._logo_src = "/logo/logo_white.png"
        else:
            self._logo_src = "/logo/logo_black.png"

        return self._logo_src

    def update_text_colors(self) -> str:
        if self._page.theme is None:
            self._page.theme = ft.Theme()

        if self._page.theme_mode == ft.ThemeMode.DARK:
            self._text_color = "white"
        else:
            self._text_color = "black"

        return self._text_color

    def app_bar(self) -> ft.AppBar:
        self.update_logo_colors()
        return ft.AppBar(
            center_title=False,
            title=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Image(src=self._logo_src, width=40, height=40),
                    ft.Container(width=10),
                    ft.Text("Noma", color=self._text_color, font_family="sf", size=18),
                ],
            ),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            text="Главная",
                            style=self._app_bar_style,
                            width=160,
                            height=50,
                            on_click=lambda e: self._page.go(
                                "/home", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.TextButton(
                            text="Начать",
                            style=self._app_bar_style,
                            width=160,
                            height=50,
                            on_click=lambda e: self._page.go(
                                "/category", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.TextButton(
                            text="О нас",
                            style=self._app_bar_style,
                            width=160,
                            height=50,
                            on_click=lambda e: self._page.go(
                                "/about", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        self._theme_button,
                    ],
                    spacing=20,
                ),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(icon=ft.Icons.PERSON_ROUNDED, text="Профиль"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            icon=ft.Icons.FILE_UPLOAD_ROUNDED,
                            text="Добавить данные",
                            on_click=lambda e: self._page.go(
                                "/category", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            icon=ft.Icons.ELECTRICAL_SERVICES_ROUNDED,
                            text="Электричество",
                            on_click=lambda e: self._page.go(
                                "/electricity", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.PopupMenuItem(
                            icon=ft.Icons.WATER_DROP_ROUNDED,
                            text="Вода",
                            on_click=lambda e: self._page.go(
                                "/water", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.PopupMenuItem(
                            icon=ft.Icons.GAS_METER_ROUNDED,
                            text="Газ",
                            on_click=lambda e: self._page.go(
                                "/gas", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            icon=ft.Icons.INFO_SHARP,
                            text="О нас",
                            on_click=lambda e: self._page.go(
                                "/about", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                    ]
                ),
            ],
        )

    def route_change(self, e: ft.ControlEvent) -> None:
        self._page.views.clear()
        route = self._page.route

        if route == "/water":

            view = asyncio.run(ResourcePage(
                self,
                resource="вода",
                label="воды",
                title="Показатели воды",
                icon=ft.Icons.WATER_DROP_ROUNDED,
                main_color="blue",
                anomaly_color="violet"
            ).build_async())
            self._page.views.append(view)
            self._page.update()
            return

        if route == "/electricity":

            view = asyncio.run(ResourcePage(
                self,
                resource="электричество",
                label="электричества",
                title="Показатели электричества",
                icon=ft.Icons.ELECTRICAL_SERVICES_ROUNDED,
                main_color="orange",
                anomaly_color="violet"
            ).build_async())
            self._page.views.append(view)
            self._page.update()
            return

        if route == "/gas":

            view = asyncio.run(ResourcePage(
                self,
                resource="газ",
                label="газа",
                title="Показатели газа",
                icon=ft.Icons.GAS_METER_ROUNDED,
                main_color="red",
                anomaly_color="violet"
            ).build_async())
            self._page.views.append(view)
            self._page.update()
            return

        view_class = self._views.get(route)
        if view_class:
            self._page.views.append(view_class(self).build())

        self._page.update()

    def run(self) -> None:
        self._page.go("/home")
