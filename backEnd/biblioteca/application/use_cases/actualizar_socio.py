"""
Caso de uso para actualizar un socio.
"""

from biblioteca.domain.repositories.socio_repository import SocioRepository
from biblioteca.application.exceptions import (
    SocioNoEncontradoError,
    RutDuplicadoError,
)


class ActualizarSocio:

    def __init__(self, repositorio: SocioRepository):
        self.repositorio = repositorio

    def ejecutar(
        self,
        id_socio: int,
        rut: str,
        nombre: str,
        email: str = None,
        telefono: str = None,
        activo: bool = None,
    ):

        socio = self.repositorio.obtener_por_id(id_socio)

        if socio is None:
            raise SocioNoEncontradoError("El socio no existe.")

        socio_existente = self.repositorio.obtener_por_rut(rut)

        if (
            socio_existente is not None
            and socio_existente.id_socio != id_socio
        ):
            raise RutDuplicadoError(
                f"El RUT {rut} ya está registrado."
            )

        socio.rut = rut
        socio.nombre = nombre
        socio.email = email
        socio.telefono = telefono

        if activo is not None:
            socio.activo = activo

        return self.repositorio.actualizar(socio)