# Proyecto: MotoTaller Pro
# Autores: Sammyr Valderrama y David Córdoba

class Cliente:
    def __init__(self, id_cliente: int | None, nombre: str, telefono: str, moto: str):
        self._id_cliente = id_cliente
        self._nombre = nombre
        self._telefono = telefono
        self._moto = moto

    @property
    def id_cliente(self) -> int | None:
        return self._id_cliente

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self._telefono = valor

    @property
    def moto(self) -> str:
        return self._moto

    @moto.setter
    def moto(self, valor: str) -> None:
        self._moto = valor

    @classmethod
    def desde_tupla(cls, fila: tuple) -> "Cliente":
        return cls(
            id_cliente=fila[0],
            nombre=fila[1],
            telefono=fila[2],
            moto=fila[3]
        )

    def __str__(self) -> str:
        return f"{self._nombre} ({self._moto})"

    def __repr__(self) -> str:
        return f"Cliente(id={self._id_cliente}, nombre='{self._nombre}', moto='{self._moto}')"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Cliente):
            return False
        return self._id_cliente == otro._id_cliente
