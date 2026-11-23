# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

from data.database_manager import DatabaseManager
from domain.producto import Producto
from domain.orden_servicio import OrdenServicio


class ProductoRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    # --- CRUD DE PRODUCTOS / REPUESTOS ---
    def crear_producto(self, producto: Producto) -> None:
        sql = "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)"
        with self.db as cursor:
            cursor.execute(sql, (producto.nombre, producto.precio, producto.stock))

    def listar_productos(self) -> list[Producto]:
        sql = "SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto DESC"
        with self.db as cursor:
            cursor.execute(sql)
            filas = cursor.fetchall()
        return [Producto.desde_tupla(fila) for fila in filas]

    def obtener_producto_por_id(self, id_producto: int) -> Producto | None:
        sql = "SELECT id_producto, nombre, precio, stock FROM productos WHERE id_producto = ?"
        with self.db as cursor:
            cursor.execute(sql, (id_producto,))
            fila = cursor.fetchone()
        return Producto.desde_tupla(fila) if fila else None

    def actualizar_producto(self, producto: Producto) -> None:
        sql = "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id_producto = ?"
        with self.db as cursor:
            cursor.execute(sql, (producto.nombre, producto.precio, producto.stock, producto.id_producto))

    def eliminar_producto(self, id_producto: int) -> None:
        sql = "DELETE FROM productos WHERE id_producto = ?"
        with self.db as cursor:
            cursor.execute(sql, (id_producto,))

    # --- CRUD DE ÓRDENES DE SERVICIO / VENTAS ---
    def registrar_orden(self, orden: OrdenServicio) -> None:
        with self.db as cursor:
            cursor.execute(
                "INSERT INTO ordenes_servicio (id_cliente, id_producto, cantidad, total, fecha) VALUES (?, ?, ?, ?, ?)",
                (orden.id_cliente, orden.id_producto, orden.cantidad, orden.total, orden.fecha)
            )
            cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE id_producto = ?",
                (orden.cantidad, orden.id_producto)
            )

    def listar_ordenes(self) -> list[OrdenServicio]:
        sql = """
            SELECT o.id_orden, o.id_cliente, o.id_producto, o.cantidad, o.total, o.fecha,
                   c.nombre, p.nombre
            FROM ordenes_servicio o
            JOIN clientes c ON o.id_cliente = c.id_cliente
            JOIN productos p ON o.id_producto = p.id_producto
            ORDER BY o.id_orden DESC
        """
        with self.db as cursor:
            cursor.execute(sql)
            filas = cursor.fetchall()
        return [OrdenServicio.desde_tupla(fila) for fila in filas]

    def eliminar_orden(self, orden: OrdenServicio) -> None:
        with self.db as cursor:
            cursor.execute("DELETE FROM ordenes_servicio WHERE id_orden = ?", (orden.id_orden,))
            cursor.execute(
                "UPDATE productos SET stock = stock + ? WHERE id_producto = ?",
                (orden.cantidad, orden.id_producto)
            )
