"""
Caso de uso para eliminar un detalle de préstamo.
"""

from django.db import transaction

from biblioteca.application.exceptions import (
    PrestamoNoEncontradoError,
    LibroNoEncontradoError,
    DetallePrestamoNoEncontradoError,
    EstadoPrestamoInvalidoError,
)


class EliminarDetallePrestamo:

    def __init__(
        self,
        detalle_repository,
        prestamo_repository,
        libro_repository,
    ):
        self.detalle_repository = detalle_repository
        self.prestamo_repository = prestamo_repository
        self.libro_repository = libro_repository

    @transaction.atomic(using="negocio")
    def ejecutar(self, id_prestamo: int, id_libro: int) -> bool:

        prestamo = self.prestamo_repository.obtener_por_id(id_prestamo)

        if prestamo is None:
            raise PrestamoNoEncontradoError("El préstamo no existe.")

        if prestamo.estado != "activo":
            raise EstadoPrestamoInvalidoError(
                "Solo se pueden eliminar detalles de préstamos activos."
            )

        detalle = self.detalle_repository.obtener_por_id(
            id_prestamo, id_libro
        )

        if detalle is None:
            raise DetallePrestamoNoEncontradoError(
                "El detalle del préstamo no existe."
            )

        libro = self.libro_repository.obtener_por_id(id_libro)

        if libro is None:
            raise LibroNoEncontradoError("El libro no existe.")

        libro.ejemplares_disponibles += detalle.cantidad

        resultado = self.libro_repository.actualizar(libro)

        if resultado is None:
            raise LibroNoEncontradoError(
                "No se pudo actualizar la disponibilidad del libro."
            )

        eliminado = self.detalle_repository.eliminar(
            id_prestamo, id_libro
        )

        if not eliminado:
            raise DetallePrestamoNoEncontradoError(
                "No se pudo eliminar el detalle del préstamo."
            )

        return True