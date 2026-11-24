
from django.db import transaction

from biblioteca.domain.entities import DetallePrestamo
from biblioteca.application.exceptions import (
    LibroNoEncontradoError,
    PrestamoNoEncontradoError,
    EjemplaresInsuficientesError,
    EstadoPrestamoInvalidoError,
    LimiteLibrosExcedidoError,
)


class CrearDetallePrestamo:

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
    def ejecutar(self, id_prestamo: int, id_libro: int, cantidad: int):

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        prestamo = self.prestamo_repository.obtener_por_id(id_prestamo)

        if prestamo is None:
            raise PrestamoNoEncontradoError("El préstamo no existe.")

        if prestamo.estado != "activo":
            raise EstadoPrestamoInvalidoError(
                "Solo se pueden agregar libros a préstamos activos."
            )

        detalles_actuales = self.detalle_repository.listar_por_prestamo(
            id_prestamo
        )

        total_actual = sum(
            detalle.cantidad for detalle in detalles_actuales
        )

        if total_actual + cantidad > 3:
            raise LimiteLibrosExcedidoError(
                "Un préstamo no puede superar los 3 libros."
            )

        libro = self.libro_repository.obtener_por_id(id_libro)

        if libro is None:
            raise LibroNoEncontradoError("El libro no existe.")

        if libro.ejemplares_disponibles < cantidad:
            raise EjemplaresInsuficientesError(
                "No hay suficientes ejemplares disponibles."
            )

        detalle = DetallePrestamo(
            id_prestamo=id_prestamo,
            id_libro=id_libro,
            cantidad=cantidad,
        )

        self.detalle_repository.guardar(detalle)

        libro.ejemplares_disponibles -= cantidad

        resultado = self.libro_repository.actualizar(libro)

        if resultado is None:
            raise LibroNoEncontradoError(
                "No se pudo actualizar la disponibilidad del libro."
            )

        return detalle
