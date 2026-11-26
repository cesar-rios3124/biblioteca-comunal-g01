"""
Caso de uso para eliminar un género literario.
"""

from biblioteca.domain.repositories.genero_repository import GeneroRepository
from biblioteca.application.exceptions import GeneroNoEncontradoError


class EliminarGenero:

    def __init__(self, repositorio: GeneroRepository):
        self.repositorio = repositorio

    def ejecutar(self, id_genero: int) -> bool:

        genero = self.repositorio.obtener_por_id(id_genero)

        if genero is None:
            raise GeneroNoEncontradoError("El género no existe.")

        eliminado = self.repositorio.eliminar(id_genero)

        if not eliminado:
            raise ValueError(
                "No se puede eliminar el género porque tiene libros asociados."
            )

        return True