# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

class OrdenServicio:
    def __init__(
        self,
        id_orden: int | None,
        id_cliente: int,
        id_producto: int,
        cantidad: int,
        total: float,
        fecha: str,
        nombre_cliente: str = "",
        nombre_producto: str = ""
    ):
        self._id_orden = id_orden
        self._id_cliente = id_cliente
        self._id_producto = id_producto
        self._cantidad = cantidad
        self._total = total
        self._fecha = fecha
        self._nombre_cliente = nombre_cliente
        self._nombre_producto = nombre_producto

    @property
    def id_orden(self) -> int | None:
        return self._id_orden

    @property
    def id_cliente(self) -> int:
        return self._id_cliente

    @property
    def id_producto(self) -> int:
        return self._id_producto

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def total(self) -> float:
        return self._total

    @property
    def fecha(self) -> str:
        return self._fecha

    @property
    def nombre_cliente(self) -> str:
        return self._nombre_cliente

    @property
    def nombre_producto(self) -> str:
        return self._nombre_producto

    @classmethod
    def desde_tupla(cls, fila: tuple) -> "OrdenServicio":
        return cls(
            id_orden=fila[0],
            id_cliente=fila[1],
            id_producto=fila[2],
            cantidad=fila[3],
            total=fila[4],
            fecha=fila[5],
            nombre_cliente=fila[6] if len(fila) > 6 else "",
            nombre_producto=fila[7] if len(fila) > 7 else ""
        )

    def __str__(self) -> str:
        return f"Orden #{self._id_orden}: {self._nombre_cliente} - {self._nombre_producto} x{self._cantidad} (${self._total:,.0f})"

    def __repr__(self) -> str:
        return f"OrdenServicio(id={self._id_orden}, cliente={self._id_cliente}, producto={self._id_producto}, total={self._total})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, OrdenServicio):
            return False
        return self._id_orden == otro._id_orden
