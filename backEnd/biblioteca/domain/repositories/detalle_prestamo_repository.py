"""
Puerto del repositorio de detalles de préstamos.
Define las operaciones que debe implementar la infraestructura.
"""

from abc import ABC, abstractmethod
from typing import Optional

from biblioteca.domain.entities import DetallePrestamo


class DetallePrestamoRepository(ABC):

    @abstractmethod
    def guardar(self, detalle: DetallePrestamo) -> DetallePrestamo:
        pass

    @abstractmethod
    def obtener_por_id(
        self, id_prestamo: int, id_libro: int
    ) -> Optional[DetallePrestamo]:
        pass

    @abstractmethod
    def listar_por_prestamo(
        self, id_prestamo: int
    ) -> list[DetallePrestamo]:
        pass

    @abstractmethod
    def actualizar(self, detalle: DetallePrestamo) -> DetallePrestamo:
        pass

    @abstractmethod
    def eliminar(self, id_prestamo: int, id_libro: int) -> bool:
        pass