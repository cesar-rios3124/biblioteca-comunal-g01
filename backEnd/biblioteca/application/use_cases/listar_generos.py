"""
Caso de uso para listar los géneros literarios de la biblioteca.
"""

from biblioteca.domain.repositories.genero_repository import GeneroRepository
from biblioteca.domain.entities import Genero


class ListarGeneros:

    def __init__(self, repositorio: GeneroRepository):
        self.repositorio = repositorio

    def ejecutar(self) -> list[Genero]:
        return self.repositorio.listar()