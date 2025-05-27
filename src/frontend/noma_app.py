import flet as ft
from view.main_page import MainView
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
        self.page.fonts = {"jura": "/fonts/Jura.ttf"}
        self.page.theme_mode = self.detect_theme_mode()

        self.theme_button = ft.IconButton(
            icon=self.get_theme_icon(), on_click=self.toggle_theme
        )

        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.page.on_route_change = self.route_change
        self.views = {
            "/": MainView,
            "/category": CategoryView,
            "/home": HomePageView,
        }

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

    def update_colors(self) -> tuple[str, str, str]:
        if self.page.theme is None:
            self.page.theme = ft.Theme()

        if self.page.theme_mode == ft.ThemeMode.DARK:
            textclr = "white"
            logo_src = "/logo/logo_white_blue.png"
            sidebar_color = "#111418"
        else:
            textclr = "black"
            logo_src = "/logo/logo_black_blue.png"
            sidebar_color = "#f8f9ff"

        return textclr, logo_src, sidebar_color

    def route_change(self, e: ft.ControlEvent) -> None:
        self.page.views.clear()
        route = self.page.route
        view_class = self.views.get(route)
        if view_class:
            self.page.views.append(view_class(self).build())
        self.page.update()

    def run(self) -> None:
        self.page.go("/")
