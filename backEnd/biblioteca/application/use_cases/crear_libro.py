"""
Caso de uso para registrar un libro en la biblioteca.
"""

from biblioteca.domain.entities import Libro
from biblioteca.domain.repositories.libro_repository import LibroRepository
from biblioteca.application.exceptions import IsbnDuplicadoError


class CrearLibro:

    def __init__(self, repositorio: LibroRepository):
        self.repositorio = repositorio

    def ejecutar(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        anio: int,
        id_genero: int,
        ejemplares_disponibles: int = 0
    ) -> Libro:

        libro_existente = self.repositorio.obtener_por_isbn(isbn)

        if libro_existente is not None:
            raise IsbnDuplicadoError(
                f"El ISBN {isbn} ya está registrado."
            )

        nuevo_libro = Libro(
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            anio=anio,
            id_genero=id_genero,
            ejemplares_disponibles=ejemplares_disponibles
        )

        return self.repositorio.guardar(nuevo_libro)