"""
Caso de uso para listar los socios de la biblioteca.
"""

from biblioteca.domain.repositories.socio_repository import SocioRepository
from biblioteca.domain.entities import Socio


class ListarSocios:

    def __init__(self, repositorio: SocioRepository):
        self.repositorio = repositorio

    def ejecutar(self) -> list[Socio]:
        return self.repositorio.listar()