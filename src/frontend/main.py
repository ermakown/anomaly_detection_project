import flet as ft
from noma_app import NomaApp


def main(page: ft.Page) -> None:
    app = NomaApp(page)
    app.run()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
