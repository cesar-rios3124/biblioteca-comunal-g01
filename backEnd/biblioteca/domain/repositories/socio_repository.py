
"""
Puerto del repositorio de socios.
Define las operaciones que debe implementar la infraestructura.
"""

from abc import ABC, abstractmethod
from typing import Optional

from biblioteca.domain.entities import Socio


class SocioRepository(ABC):

    @abstractmethod
    def guardar(self, socio: Socio) -> Socio:
        pass

    @abstractmethod
    def obtener_por_id(self, id_socio: int) -> Optional[Socio]:
        pass

    @abstractmethod
    def obtener_por_rut(self, rut: str) -> Optional[Socio]:
        pass

    @abstractmethod
    def listar(self) -> list[Socio]:
        pass

    @abstractmethod
    def actualizar(self, socio: Socio) -> Socio:
        pass

    @abstractmethod
    def eliminar(self, id_socio: int) -> bool:
        pass
