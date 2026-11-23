# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

from data.database_manager import DatabaseManager
from domain.cliente import Cliente


class ClienteDAO:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def crear(self, cliente: Cliente) -> None:
        sql = "INSERT INTO clientes (nombre, telefono, moto) VALUES (?, ?, ?)"
        with self.db as cursor:
            cursor.execute(sql, (cliente.nombre, cliente.telefono, cliente.moto))

    def listar_todos(self) -> list[Cliente]:
        sql = "SELECT id_cliente, nombre, telefono, moto FROM clientes ORDER BY id_cliente DESC"
        with self.db as cursor:
            cursor.execute(sql)
            filas = cursor.fetchall()
        return [Cliente.desde_tupla(fila) for fila in filas]

    def actualizar(self, cliente: Cliente) -> None:
        sql = "UPDATE clientes SET nombre = ?, telefono = ?, moto = ? WHERE id_cliente = ?"
        with self.db as cursor:
            cursor.execute(sql, (cliente.nombre, cliente.telefono, cliente.moto, cliente.id_cliente))

    def eliminar(self, id_cliente: int) -> None:
        sql = "DELETE FROM clientes WHERE id_cliente = ?"
        with self.db as cursor:
            cursor.execute(sql, (id_cliente,))
