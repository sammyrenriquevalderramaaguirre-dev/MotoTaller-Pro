# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

import flet as ft
from ui.app_view import AppView


def main(page: ft.Page) -> None:
    AppView(page)


if __name__ == "__main__":
    ft.app(target=main)
