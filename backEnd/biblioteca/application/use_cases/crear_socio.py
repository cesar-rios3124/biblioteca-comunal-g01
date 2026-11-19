
"""
Caso de uso para registrar un socio en la biblioteca.
"""

from biblioteca.domain.entities import Socio
from biblioteca.domain.repositories.socio_repository import SocioRepository
from biblioteca.application.exceptions import RutDuplicadoError


class CrearSocio:

    def __init__(self, repositorio: SocioRepository):
        self.repositorio = repositorio

    def ejecutar(
        self,
        rut: str,
        nombre: str,
        email: str = None,
        telefono: str = None
    ) -> Socio:

        socio_existente = self.repositorio.obtener_por_rut(rut)

        if socio_existente is not None:
            raise RutDuplicadoError(
                f"El RUT {rut} ya está registrado."
            )

        nuevo_socio = Socio(
            rut=rut,
            nombre=nombre,
            email=email,
            telefono=telefono
        )

        return self.repositorio.guardar(nuevo_socio)
