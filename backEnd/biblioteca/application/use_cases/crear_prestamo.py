
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from biblioteca.domain.entities import Prestamo
from biblioteca.application.exceptions import (
    SocioNoEncontradoError,
    SocioInactivoError,
    SocioConPrestamoAtrasadoError,
)
from biblioteca.application.use_cases.crear_detalle_prestamo import (
    CrearDetallePrestamo,
)


class CrearPrestamo:

    def __init__(
        self,
        prestamo_repository,
        socio_repository,
        detalle_repository,
        libro_repository,
    ):
        self.prestamo_repository = prestamo_repository
        self.socio_repository = socio_repository

        self.crear_detalle = CrearDetallePrestamo(
            detalle_repository,
            prestamo_repository,
            libro_repository,
        )

    @transaction.atomic(using="negocio")
    def ejecutar(self, id_socio: int, detalles: list[tuple[int, int]]):

        if not detalles:
            raise ValueError("El préstamo debe incluir al menos un libro.")

        socio = self.socio_repository.obtener_por_id(id_socio)

        if socio is None:
            raise SocioNoEncontradoError("El socio no existe.")

        if not socio.activo:
            raise SocioInactivoError(
                "El socio está inactivo y no puede solicitar préstamos."
            )
        
        self.prestamo_repository.marcar_atrasados()
        
        prestamos = self.prestamo_repository.listar_por_socio(id_socio)

        if any(prestamo.estado == "atrasado" for prestamo in prestamos):
            raise SocioConPrestamoAtrasadoError(
                "El socio tiene un préstamo atrasado."
            )

        fecha_actual = timezone.now()

        prestamo = Prestamo(
            id_socio=id_socio,
            fecha_prestamo=fecha_actual,
            fecha_devolucion_esperada=fecha_actual + timedelta(days=14),
            estado="activo",
        )

        prestamo = self.prestamo_repository.guardar(prestamo)

        for id_libro, cantidad in detalles:
            self.crear_detalle.ejecutar(
                id_prestamo=prestamo.id_prestamo,
                id_libro=id_libro,
                cantidad=cantidad,
            )

        return prestamo
