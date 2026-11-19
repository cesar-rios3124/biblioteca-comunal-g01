"""
Puerto del repositorio de libros.
Define las operaciones que debe implementar la infraestructura.
"""

from abc import ABC, abstractmethod
from typing import Optional

from biblioteca.domain.entities import Libro


class LibroRepository(ABC):

    @abstractmethod
    def guardar(self, libro: Libro) -> Libro:
        pass

    @abstractmethod
    def obtener_por_id(self, id_libro: int) -> Optional[Libro]:
        pass

    @abstractmethod
    def obtener_por_isbn(self, isbn: str) -> Optional[Libro]:
        pass

    @abstractmethod
    def listar(self) -> list[Libro]:
        pass

    @abstractmethod
    def actualizar(self, libro: Libro) -> Libro:
        pass

    @abstractmethod
    def eliminar(self, id_libro: int) -> bool:
        pass