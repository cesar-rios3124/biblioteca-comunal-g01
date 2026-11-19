"""
Caso de uso para listar los libros de la biblioteca.
"""

from biblioteca.domain.repositories.libro_repository import LibroRepository
from biblioteca.domain.entities import Libro


class ListarLibros:

    def __init__(self, repositorio: LibroRepository):
        self.repositorio = repositorio

    def ejecutar(self) -> list[Libro]:
        return self.repositorio.listar()