# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

import flet as ft


def crear_tabla(columnas: list[str], filas: list[ft.DataRow]) -> ft.DataTable:
    return ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD)) for col in columnas],
        rows=filas,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        heading_row_color=ft.Colors.BLUE_GREY_50,
    )
