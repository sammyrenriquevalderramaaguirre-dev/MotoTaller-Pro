# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

class Producto:
    def __init__(self, id_producto: int | None, nombre: str, precio: float, stock: int):
        self._id_producto = id_producto
        self._nombre = nombre
        self._precio = precio
        self._stock = stock

    @property
    def id_producto(self) -> int | None:
        return self._id_producto

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = valor

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        self._precio = valor

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        self._stock = valor

    @classmethod
    def desde_tupla(cls, fila: tuple) -> "Producto":
        return cls(
            id_producto=fila[0],
            nombre=fila[1],
            precio=fila[2],
            stock=fila[3]
        )

    def __str__(self) -> str:
        return f"{self._nombre} - ${self._precio:,.0f} (Stock: {self._stock})"

    def __repr__(self) -> str:
        return f"Producto(id={self._id_producto}, nombre='{self._nombre}', precio={self._precio}, stock={self._stock})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Producto):
            return False
        return self._id_producto == otro._id_producto

    def __len__(self) -> int:
        return self._stock
