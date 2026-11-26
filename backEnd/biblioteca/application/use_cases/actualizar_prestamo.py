"""
Caso de uso para actualizar la fecha de devolución esperada.
"""

from biblioteca.domain.repositories.prestamo_repository import PrestamoRepository
from biblioteca.application.exceptions import (
    PrestamoNoEncontradoError,
    EstadoPrestamoInvalidoError,
)


class ActualizarPrestamo:

    def __init__(self, repositorio: PrestamoRepository):
        self.repositorio = repositorio

    def ejecutar(self, id_prestamo: int, nueva_fecha):

        prestamo = self.repositorio.obtener_por_id(id_prestamo)

        if prestamo is None:
            raise PrestamoNoEncontradoError("El préstamo no existe.")

        if prestamo.estado != "activo":
            raise EstadoPrestamoInvalidoError(
                "Solo se pueden modificar préstamos activos."
            )

        prestamo.fecha_devolucion_esperada = nueva_fecha

        return self.repositorio.actualizar(prestamo)