"""
Puerto del repositorio de préstamos.
Define las operaciones que debe implementar la infraestructura.
"""

from abc import ABC, abstractmethod
from typing import Optional

from biblioteca.domain.entities import Prestamo


class PrestamoRepository(ABC):

    @abstractmethod
    def guardar(self, prestamo: Prestamo) -> Prestamo:
        pass

    @abstractmethod
    def obtener_por_id(self, id_prestamo: int) -> Optional[Prestamo]:
        pass

    @abstractmethod
    def listar(self) -> list[Prestamo]:
        pass

    @abstractmethod
    def listar_por_socio(self, id_socio: int) -> list[Prestamo]:
        pass

    @abstractmethod
    def actualizar(self, prestamo: Prestamo) -> Prestamo:
        pass

    @abstractmethod
    def eliminar(self, id_prestamo: int) -> bool:
        pass