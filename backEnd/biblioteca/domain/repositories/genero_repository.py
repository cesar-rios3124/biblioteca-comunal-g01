
"""
Puerto del repositorio de géneros.
Define las operaciones que debe implementar la infraestructura.
"""

from abc import ABC, abstractmethod
from typing import Optional

from biblioteca.domain.entities import Genero


class GeneroRepository(ABC):

    @abstractmethod
    def guardar(self, genero: Genero) -> Genero:
        pass

    @abstractmethod
    def obtener_por_id(self, id_genero: int) -> Optional[Genero]:
        pass

    @abstractmethod
    def listar(self) -> list[Genero]:
        pass

    @abstractmethod
    def actualizar(self, genero: Genero) -> Genero:
        pass

    @abstractmethod
    def eliminar(self, id_genero: int) -> bool:
        pass
