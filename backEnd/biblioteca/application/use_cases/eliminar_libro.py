"""
Caso de uso para eliminar un libro.
"""

from biblioteca.domain.repositories.libro_repository import LibroRepository
from biblioteca.application.exceptions import LibroNoEncontradoError


class EliminarLibro:

    def __init__(self, repositorio: LibroRepository):
        self.repositorio = repositorio

    def ejecutar(self, id_libro: int) -> bool:

        libro = self.repositorio.obtener_por_id(id_libro)

        if libro is None:
            raise LibroNoEncontradoError("El libro no existe.")

        eliminado = self.repositorio.eliminar(id_libro)

        if not eliminado:
            raise ValueError(
                "No se puede eliminar el libro porque tiene detalles de préstamo asociados."
            )

        return True