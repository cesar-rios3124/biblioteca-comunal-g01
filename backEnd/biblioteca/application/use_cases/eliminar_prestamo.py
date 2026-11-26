"""
Caso de uso para eliminar un préstamo.
"""

from biblioteca.domain.repositories.prestamo_repository import PrestamoRepository
from biblioteca.domain.repositories.detalle_prestamo_repository import (
    DetallePrestamoRepository,
)
from biblioteca.application.exceptions import PrestamoNoEncontradoError


class EliminarPrestamo:

    def __init__(
        self,
        prestamo_repository: PrestamoRepository,
        detalle_repository: DetallePrestamoRepository,
    ):
        self.prestamo_repository = prestamo_repository
        self.detalle_repository = detalle_repository

    def ejecutar(self, id_prestamo: int) -> bool:

        prestamo = self.prestamo_repository.obtener_por_id(id_prestamo)

        if prestamo is None:
            raise PrestamoNoEncontradoError("El préstamo no existe.")

        detalles = self.detalle_repository.listar_por_prestamo(id_prestamo)

        if detalles:
            raise ValueError(
                "No se puede eliminar el préstamo porque tiene detalles asociados."
            )

        return self.prestamo_repository.eliminar(id_prestamo)