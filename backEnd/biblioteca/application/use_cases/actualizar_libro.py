"""
Caso de uso para actualizar un libro.
"""

from biblioteca.domain.repositories.libro_repository import LibroRepository
from biblioteca.application.exceptions import (
    LibroNoEncontradoError,
    IsbnDuplicadoError,
)


class ActualizarLibro:

    def __init__(self, repositorio: LibroRepository):
        self.repositorio = repositorio

    def ejecutar(
        self,
        id_libro: int,
        isbn: str,
        titulo: str,
        autor: str,
        anio: int,
        id_genero: int,
        ejemplares_disponibles: int,
    ):

        libro = self.repositorio.obtener_por_id(id_libro)

        if libro is None:
            raise LibroNoEncontradoError("El libro no existe.")

        libro_existente = self.repositorio.obtener_por_isbn(isbn)

        if libro_existente is not None and libro_existente.id_libro != id_libro:
            raise IsbnDuplicadoError(
                f"El ISBN {isbn} ya está registrado."
            )

        libro.isbn = isbn
        libro.titulo = titulo
        libro.autor = autor
        libro.anio = anio
        libro.id_genero = id_genero
        libro.ejemplares_disponibles = ejemplares_disponibles

        return self.repositorio.actualizar(libro)