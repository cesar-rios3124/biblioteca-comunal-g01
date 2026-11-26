"""
Caso de uso para actualizar un género literario.
"""

from biblioteca.domain.repositories.genero_repository import GeneroRepository
from biblioteca.application.exceptions import (
    GeneroNoEncontradoError,
    GeneroDuplicadoError,
)


class ActualizarGenero:

    def __init__(self, repositorio: GeneroRepository):
        self.repositorio = repositorio

    def ejecutar(self, id_genero: int, nombre: str):

        genero = self.repositorio.obtener_por_id(id_genero)

        if genero is None:
            raise GeneroNoEncontradoError("El género no existe.")

        generos = self.repositorio.listar()

        for existente in generos:
            if existente.nombre.lower() == nombre.lower() and existente.id_genero != id_genero:
                raise GeneroDuplicadoError(
                    f"El género {nombre} ya está registrado."
                )

        genero.nombre = nombre

        return self.repositorio.actualizar(genero)