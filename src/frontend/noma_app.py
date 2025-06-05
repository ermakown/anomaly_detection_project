from typing import Union
import flet as ft
from view.category_page import CategoryView
from view.home import HomePageView


class NomaApp:
    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.page.title = "Noma"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.fonts = {"jura": "/fonts/Jura.ttf", "sf": "/fonts/System Font.ttf"}
        self.page.theme_mode = self.detect_theme_mode()
        self.textclr: None | str = None
        self.logo_src: None | str = None

        self.theme_button = ft.IconButton(
            icon=self.get_theme_icon(), on_click=self.toggle_theme
        )

        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.page.on_route_change = self.route_change
        self.views = {
            "/category": CategoryView,
            "/home": HomePageView,
        }

        self.app_bar_style = ft.ButtonStyle(
            text_style=ft.TextStyle(color=self.textclr, size=18, font_family="sf")
        )

    def detect_theme_mode(self) -> ft.ThemeMode:

        return (
            ft.ThemeMode.DARK
            if self.page.platform_brightness == ft.Brightness.DARK
            else ft.ThemeMode.LIGHT
        )

    def get_theme_icon(self) -> ft.Icons:
        return (
            ft.Icons.LIGHT_MODE_ROUNDED
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ft.Icons.NIGHTLIGHT_ROUND_ROUNDED
        )

    def toggle_theme(self, e: ft.ControlEvent) -> None:

        self.page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        self.theme_button.icon = self.get_theme_icon()
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
        if self.page.theme is None:
            self.page.theme = ft.Theme()

        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.logo_src = "/logo/logo_white.png"
        else:
            self.logo_src = "/logo/logo_black.png"

        return self.logo_src

    def update_text_colors(self) -> str:
        if self.page.theme is None:
            self.page.theme = ft.Theme()

        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.textclr = "white"
        else:
            self.textclr = "black"

        return self.textclr

    def app_bar(self) -> ft.AppBar:
        self.update_logo_colors()
        return ft.AppBar(
            center_title=False,
            title=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Image(src=self.logo_src, width=40, height=40),
                    ft.Container(width=10),
                    ft.Text("Noma", color=self.textclr, font_family="sf", size=18),
                ],
            ),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            text="Начать",
                            style=self.app_bar_style,
                            width=160,
                            height=50,
                            on_click=lambda e: self.page.go(
                                "/category", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.TextButton(
                            text="Главная",
                            style=self.app_bar_style,
                            width=160,
                            height=50,
                            on_click=lambda e: self.page.go(
                                "/home", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        self.theme_button,
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
                            on_click=lambda e: self.page.go(
                                "/category", ft.PageTransitionTheme.PREDICTIVE
                            ),
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=ft.Icons.WATER_DROP_ROUNDED, text="Вода"),
                        ft.PopupMenuItem(
                            icon=ft.Icons.ELECTRICAL_SERVICES_ROUNDED,
                            text="Электричество",
                        ),
                        ft.PopupMenuItem(icon=ft.Icons.GAS_METER_ROUNDED, text="Газ"),
                    ]
                ),
            ],
        )

    def route_change(self, e: ft.ControlEvent) -> None:
        self.page.views.clear()
        route = self.page.route
        view_class = self.views.get(route)
        if view_class:
            self.page.views.append(view_class(self).build())
        self.page.update()

    def run(self) -> None:
        self.page.go("/home")
