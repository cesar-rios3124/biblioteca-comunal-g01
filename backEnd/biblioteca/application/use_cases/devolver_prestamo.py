
from django.db import transaction

from biblioteca.application.exceptions import (
    PrestamoNoEncontradoError,
    LibroNoEncontradoError,
    EstadoPrestamoInvalidoError,
)


class DevolverPrestamo:
    def __init__(self, prestamo_repository, detalle_repository, libro_repository):
        self.prestamo_repository = prestamo_repository
        self.detalle_repository = detalle_repository
        self.libro_repository = libro_repository

    @transaction.atomic(using="negocio")
    def ejecutar(self, id_prestamo: int):
        prestamo = self.prestamo_repository.obtener_por_id(id_prestamo)

        if prestamo is None:
            raise PrestamoNoEncontradoError("El préstamo no existe.")

        if prestamo.estado not in ("activo", "atrasado"):
            raise EstadoPrestamoInvalidoError(
                "Este préstamo no se encuentra en un estado válido para devolver."
            )

        detalles = self.detalle_repository.listar_por_prestamo(id_prestamo)

        for detalle in detalles:
            libro = self.libro_repository.obtener_por_id(detalle.id_libro)

            if libro is None:
                raise LibroNoEncontradoError(
                    f"No se encontró el libro con ID {detalle.id_libro}."
                )

            libro.ejemplares_disponibles += detalle.cantidad

            resultado = self.libro_repository.actualizar(libro)

            if resultado is None:
                raise LibroNoEncontradoError(
                    "No se pudo actualizar la disponibilidad del libro."
                )

        prestamo.estado = "devuelto"

        resultado = self.prestamo_repository.actualizar(prestamo)

        if resultado is None:
            raise PrestamoNoEncontradoError(
                "No se pudo actualizar el estado del préstamo."
            )

        return prestamo
