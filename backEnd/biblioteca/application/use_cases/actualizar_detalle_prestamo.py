"""
Caso de uso para actualizar la cantidad de un detalle de préstamo.
"""

from django.db import transaction

from biblioteca.application.exceptions import (
    PrestamoNoEncontradoError,
    LibroNoEncontradoError,
    DetallePrestamoNoEncontradoError,
    EstadoPrestamoInvalidoError,
    EjemplaresInsuficientesError,
    LimiteLibrosExcedidoError,
)


class ActualizarDetallePrestamo:

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
    def ejecutar(self, id_prestamo: int, id_libro: int, nueva_cantidad: int):

        if nueva_cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        prestamo = self.prestamo_repository.obtener_por_id(id_prestamo)

        if prestamo is None:
            raise PrestamoNoEncontradoError("El préstamo no existe.")

        if prestamo.estado != "activo":
            raise EstadoPrestamoInvalidoError(
                "Solo se pueden modificar detalles de préstamos activos."
            )

        detalle = self.detalle_repository.obtener_por_id(
            id_prestamo, id_libro
        )

        if detalle is None:
            raise DetallePrestamoNoEncontradoError(
                "El detalle del préstamo no existe."
            )

        detalles = self.detalle_repository.listar_por_prestamo(id_prestamo)

        total_actual = sum(item.cantidad for item in detalles)
        diferencia = nueva_cantidad - detalle.cantidad

        if total_actual + diferencia > 3:
            raise LimiteLibrosExcedidoError(
                "Un préstamo no puede superar los 3 libros."
            )

        libro = self.libro_repository.obtener_por_id(id_libro)

        if libro is None:
            raise LibroNoEncontradoError("El libro no existe.")

        if diferencia > 0 and libro.ejemplares_disponibles < diferencia:
            raise EjemplaresInsuficientesError(
                "No hay suficientes ejemplares disponibles."
            )

        libro.ejemplares_disponibles -= diferencia
        resultado = self.libro_repository.actualizar(libro)

        if resultado is None:
            raise LibroNoEncontradoError(
                "No se pudo actualizar la disponibilidad del libro."
            )

        detalle.cantidad = nueva_cantidad

        return self.detalle_repository.actualizar(detalle)