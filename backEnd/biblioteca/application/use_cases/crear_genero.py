"""
Caso de uso para registrar un género literario.
"""

from biblioteca.domain.entities import Genero
from biblioteca.domain.repositories.genero_repository import GeneroRepository
from biblioteca.application.exceptions import GeneroDuplicadoError


class CrearGenero:

    def __init__(self, repositorio: GeneroRepository):
        self.repositorio = repositorio

    def ejecutar(self, nombre: str) -> Genero:

        generos = self.repositorio.listar()

        for genero in generos:
            if genero.nombre.lower() == nombre.lower():
                raise GeneroDuplicadoError(
                    f"El género {nombre} ya está registrado."
                )

        nuevo_genero = Genero(nombre=nombre)

        return self.repositorio.guardar(nuevo_genero)