
from datetime import timedelta

from django.utils import timezone

from biblioteca.domain.entities import Prestamo
from biblioteca.application.exceptions import (
    SocioNoEncontradoError,
    SocioInactivoError,
    SocioConPrestamoAtrasadoError,
)


class CrearPrestamo:
    def __init__(self, prestamo_repository, socio_repository):
        self.prestamo_repository = prestamo_repository
        self.socio_repository = socio_repository

    def ejecutar(self, id_socio: int):
        socio = self.socio_repository.obtener_por_id(id_socio)

        if socio is None:
            raise SocioNoEncontradoError("El socio no existe.")

        if not socio.activo:
            raise SocioInactivoError(
                "El socio está inactivo y no puede solicitar préstamos."
            )

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

        return self.prestamo_repository.guardar(prestamo)
