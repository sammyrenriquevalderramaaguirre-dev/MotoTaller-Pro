# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

from datetime import datetime
import sqlite3
import flet as ft

from data.database_manager import DatabaseManager
from data.cliente_dao import ClienteDAO
from data.producto_repository import ProductoRepository
from domain.cliente import Cliente
from domain.producto import Producto
from domain.orden_servicio import OrdenServicio
from ui.components.tabla_generica import crear_tabla


class AppView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "MotoTaller Pro - Sammyr Valderrama & David Córdoba"
        self.page.window_width = 1050
        self.page.window_height = 720
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO

        # Persistencia
        self.db = DatabaseManager()
        self.db.inicializar_tablas()
        self.cliente_dao = ClienteDAO(self.db)
        self.producto_repo = ProductoRepository(self.db)

        # Estados para edición
        self.cliente_editando_id: int | None = None
        self.producto_editando_id: int | None = None

        self._construir_interfaz()
        self.refrescar_todo()

    def mostrar_mensaje(self, texto: str, es_error: bool = False) -> None:
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(texto, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700 if es_error else ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _construir_interfaz(self) -> None:
        # --- CONTROLES CLIENTES ---
        self.txt_cli_nombre = ft.TextField(label="Nombre del cliente", width=220)
        self.txt_cli_telefono = ft.TextField(label="Teléfono", width=180)
        self.txt_cli_moto = ft.TextField(label="Moto (Ej: AKT Dynamic 125)", width=240)
        self.btn_cli_guardar = ft.ElevatedButton("Guardar Cliente", on_click=self.guardar_cliente)
        self.btn_cli_cancelar = ft.TextButton("Cancelar", visible=False, on_click=self.cancelar_edicion_cliente)
        self.contenedor_tabla_clientes = ft.Column()

        tab_clientes = ft.Column([
            ft.Text("Registro y Gestión de Clientes", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.txt_cli_nombre,
                self.txt_cli_telefono,
                self.txt_cli_moto,
                self.btn_cli_guardar,
                self.btn_cli_cancelar
            ], wrap=True),
            ft.Divider(),
            self.contenedor_tabla_clientes
        ], spacing=15)

        # --- CONTROLES PRODUCTOS / REPUESTOS ---
        self.txt_prod_nombre = ft.TextField(label="Repuesto o Servicio", width=250)
        self.txt_prod_precio = ft.TextField(label="Precio ($)", width=160)
        self.txt_prod_stock = ft.TextField(label="Stock disponible", width=160)
        self.btn_prod_guardar = ft.ElevatedButton("Guardar Repuesto", on_click=self.guardar_producto)
        self.btn_prod_cancelar = ft.TextButton("Cancelar", visible=False, on_click=self.cancelar_edicion_producto)
        self.contenedor_tabla_productos = ft.Column()

        tab_productos = ft.Column([
            ft.Text("Inventario de Repuestos y Servicios", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.txt_prod_nombre,
                self.txt_prod_precio,
                self.txt_prod_stock,
                self.btn_prod_guardar,
                self.btn_prod_cancelar
            ], wrap=True),
            ft.Divider(),
            self.contenedor_tabla_productos
        ], spacing=15)

        # --- CONTROLES ÓRDENES DE SERVICIO ---
        self.dd_orden_cliente = ft.Dropdown(label="Seleccionar Cliente", width=260)
        self.dd_orden_producto = ft.Dropdown(label="Seleccionar Repuesto/Servicio", width=280)
        self.txt_orden_cantidad = ft.TextField(label="Cantidad", value="1", width=120)
        self.btn_orden_crear = ft.ElevatedButton("Registrar Orden", on_click=self.crear_orden)
        self.contenedor_tabla_ordenes = ft.Column()

        tab_ordenes = ft.Column([
            ft.Text("Órdenes de Servicio y Facturación", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.dd_orden_cliente,
                self.dd_orden_producto,
                self.txt_orden_cantidad,
                self.btn_orden_crear
            ], wrap=True),
            ft.Divider(),
            self.contenedor_tabla_ordenes
        ], spacing=15)

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            tabs=[
                ft.Tab(text="Clientes", content=ft.Container(content=tab_clientes, padding=15)),
                ft.Tab(text="Repuestos / Stock", content=ft.Container(content=tab_productos, padding=15)),
                ft.Tab(text="Órdenes de Servicio", content=ft.Container(content=tab_ordenes, padding=15)),
            ],
            expand=True
        )

        self.page.add(
            ft.Row([
                ft.Text("MotoTaller Pro - Sistema de Gestión", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Desarrollado por: Sammyr Valderrama y David Córdoba", size=12, color=ft.Colors.GREY_700)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            tabs
        )

    # --- LÓGICA CLIENTES ---
    def guardar_cliente(self, e) -> None:
        nombre = self.txt_cli_nombre.value.strip()
        telefono = self.txt_cli_telefono.value.strip()
        moto = self.txt_cli_moto.value.strip()

        if not nombre or not telefono or not moto:
            self.mostrar_mensaje("Todos los campos del cliente son obligatorios.", es_error=True)
            return

        if self.cliente_editando_id is None:
            self.cliente_dao.crear(Cliente(None, nombre, telefono, moto))
            self.mostrar_mensaje("Cliente registrado correctamente.")
        else:
            self.cliente_dao.actualizar(Cliente(self.cliente_editando_id, nombre, telefono, moto))
            self.mostrar_mensaje("Cliente actualizado correctamente.")
            self.cancelar_edicion_cliente(None)

        self.txt_cli_nombre.value = ""
        self.txt_cli_telefono.value = ""
        self.txt_cli_moto.value = ""
        self.refrescar_todo()

    def preparar_edicion_cliente(self, cliente: Cliente) -> None:
        self.cliente_editando_id = cliente.id_cliente
        self.txt_cli_nombre.value = cliente.nombre
        self.txt_cli_telefono.value = cliente.telefono
        self.txt_cli_moto.value = cliente.moto
        self.btn_cli_guardar.text = "Actualizar Cliente"
        self.btn_cli_cancelar.visible = True
        self.page.update()

    def cancelar_edicion_cliente(self, e) -> None:
        self.cliente_editando_id = None
        self.txt_cli_nombre.value = ""
        self.txt_cli_telefono.value = ""
        self.txt_cli_moto.value = ""
        self.btn_cli_guardar.text = "Guardar Cliente"
        self.btn_cli_cancelar.visible = False
        self.page.update()

    def eliminar_cliente(self, id_cliente: int) -> None:
        try:
            self.cliente_dao.eliminar(id_cliente)
            self.mostrar_mensaje("Cliente eliminado.")
            self.refrescar_todo()
        except sqlite3.IntegrityError:
            self.mostrar_mensaje("No se puede eliminar: el cliente tiene órdenes asociadas.", es_error=True)

    # --- LÓGICA PRODUCTOS ---
    def guardar_producto(self, e) -> None:
        nombre = self.txt_prod_nombre.value.strip()
        precio_txt = self.txt_prod_precio.value.strip()
        stock_txt = self.txt_prod_stock.value.strip()

        if not nombre or not precio_txt or not stock_txt:
            self.mostrar_mensaje("Completa todos los campos del repuesto.", es_error=True)
            return

        try:
            precio = float(precio_txt)
            stock = int(stock_txt)
            if precio < 0 or stock < 0:
                raise ValueError
        except ValueError:
            self.mostrar_mensaje("Precio y stock deben ser números positivos.", es_error=True)
            return

        if self.producto_editando_id is None:
            self.producto_repo.crear_producto(Producto(None, nombre, precio, stock))
            self.mostrar_mensaje("Repuesto guardado.")
        else:
            self.producto_repo.actualizar_producto(Producto(self.producto_editando_id, nombre, precio, stock))
            self.mostrar_mensaje("Repuesto actualizado.")
            self.cancelar_edicion_producto(None)

        self.txt_prod_nombre.value = ""
        self.txt_prod_precio.value = ""
        self.txt_prod_stock.value = ""
        self.refrescar_todo()

    def preparar_edicion_producto(self, producto: Producto) -> None:
        self.producto_editando_id = producto.id_producto
        self.txt_prod_nombre.value = producto.nombre
        self.txt_prod_precio.value = str(producto.precio)
        self.txt_prod_stock.value = str(producto.stock)
        self.btn_prod_guardar.text = "Actualizar Repuesto"
        self.btn_prod_cancelar.visible = True
        self.page.update()

    def cancelar_edicion_producto(self, e) -> None:
        self.producto_editando_id = None
        self.txt_prod_nombre.value = ""
        self.txt_prod_precio.value = ""
        self.txt_prod_stock.value = ""
        self.btn_prod_guardar.text = "Guardar Repuesto"
        self.btn_prod_cancelar.visible = False
        self.page.update()

    def eliminar_producto(self, id_producto: int) -> None:
        try:
            self.producto_repo.eliminar_producto(id_producto)
            self.mostrar_mensaje("Repuesto eliminado.")
            self.refrescar_todo()
        except sqlite3.IntegrityError:
            self.mostrar_mensaje("No se puede eliminar: el repuesto está en órdenes registradas.", es_error=True)

    # --- LÓGICA ÓRDENES ---
    def crear_orden(self, e) -> None:
        if not self.dd_orden_cliente.value or not self.dd_orden_producto.value:
            self.mostrar_mensaje("Selecciona un cliente y un repuesto.", es_error=True)
            return

        try:
            cantidad = int(self.txt_orden_cantidad.value.strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            self.mostrar_mensaje("La cantidad debe ser un entero mayor a 0.", es_error=True)
            return

        id_cliente = int(self.dd_orden_cliente.value)
        id_producto = int(self.dd_orden_producto.value)
        producto = self.producto_repo.obtener_producto_por_id(id_producto)

        if not producto or len(producto) < cantidad:
            self.mostrar_mensaje("Stock insuficiente para realizar la orden.", es_error=True)
            return

        total = producto.precio * cantidad
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        orden = OrdenServicio(None, id_cliente, id_producto, cantidad, total, fecha)

        self.producto_repo.registrar_orden(orden)
        self.txt_orden_cantidad.value = "1"
        self.mostrar_mensaje("Orden registrada y stock actualizado.")
        self.refrescar_todo()

    def eliminar_orden(self, orden: OrdenServicio) -> None:
        self.producto_repo.eliminar_orden(orden)
        self.mostrar_mensaje("Orden anulada y stock devuelto.")
        self.refrescar_todo()

    # --- REFRESCO DINÁMICO ---
    def refrescar_todo(self) -> None:
        clientes = self.cliente_dao.listar_todos()
        productos = self.producto_repo.listar_productos()
        ordenes = self.producto_repo.listar_ordenes()

        # Tabla Clientes
        filas_cli = []
        for c in clientes:
            filas_cli.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(c.id_cliente))),
                ft.DataCell(ft.Text(c.nombre)),
                ft.DataCell(ft.Text(c.telefono)),
                ft.DataCell(ft.Text(c.moto)),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, obj=c: self.preparar_edicion_cliente(obj)),
                    ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", icon_color=ft.Colors.RED, on_click=lambda e, cid=c.id_cliente: self.eliminar_cliente(cid)),
                ]))
            ]))
        self.contenedor_tabla_clientes.controls = [
            crear_tabla(["ID", "Nombre", "Teléfono", "Moto", "Acciones"], filas_cli)
        ]

        # Tabla Productos
        filas_prod = []
        for p in productos:
            filas_prod.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(p.id_producto))),
                ft.DataCell(ft.Text(p.nombre)),
                ft.DataCell(ft.Text(f"${p.precio:,.0f}")),
                ft.DataCell(ft.Text(str(p.stock))),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, obj=p: self.preparar_edicion_producto(obj)),
                    ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", icon_color=ft.Colors.RED, on_click=lambda e, pid=p.id_producto: self.eliminar_producto(pid)),
                ]))
            ]))
        self.contenedor_tabla_productos.controls = [
            crear_tabla(["ID", "Repuesto / Servicio", "Precio", "Stock", "Acciones"], filas_prod)
        ]

        # Dropdowns de Órdenes
        self.dd_orden_cliente.options = [
            ft.dropdown.Option(key=str(c.id_cliente), text=str(c)) for c in clientes
        ]
        self.dd_orden_producto.options = [
            ft.dropdown.Option(key=str(p.id_producto), text=str(p)) for p in productos
        ]

        # Tabla Órdenes
        filas_ord = []
        for o in ordenes:
            filas_ord.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(o.id_orden))),
                ft.DataCell(ft.Text(o.nombre_cliente)),
                ft.DataCell(ft.Text(o.nombre_producto)),
                ft.DataCell(ft.Text(str(o.cantidad))),
                ft.DataCell(ft.Text(f"${o.total:,.0f}")),
                ft.DataCell(ft.Text(o.fecha)),
                ft.DataCell(
                    ft.IconButton(ft.Icons.DELETE, tooltip="Anular Orden", icon_color=ft.Colors.RED, on_click=lambda e, obj=o: self.eliminar_orden(obj))
                )
            ]))
        self.contenedor_tabla_ordenes.controls = [
            crear_tabla(["ID", "Cliente", "Repuesto/Servicio", "Cant.", "Total", "Fecha", "Acción"], filas_ord)
        ]

        self.page.update()
