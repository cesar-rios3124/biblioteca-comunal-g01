
"""
Caso de uso para listar los préstamos de la biblioteca.
"""

from biblioteca.domain.repositories.prestamo_repository import PrestamoRepository
from biblioteca.domain.entities import Prestamo


class ListarPrestamos:

    def __init__(self, repositorio: PrestamoRepository):
        self.repositorio = repositorio

    def ejecutar(self) -> list[Prestamo]:
        # Actualizar el estado de los préstamos vencidos.
        self.repositorio.marcar_atrasados()

        # Listar los préstamos con sus estados actualizados.
        return self.repositorio.listar()
