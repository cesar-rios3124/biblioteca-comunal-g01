"""
Caso de uso para eliminar un socio.
"""

from biblioteca.domain.repositories.socio_repository import SocioRepository
from biblioteca.application.exceptions import SocioNoEncontradoError


class EliminarSocio:

    def __init__(self, repositorio: SocioRepository):
        self.repositorio = repositorio

    def ejecutar(self, id_socio: int) -> bool:

        socio = self.repositorio.obtener_por_id(id_socio)

        if socio is None:
            raise SocioNoEncontradoError("El socio no existe.")

        eliminado = self.repositorio.eliminar(id_socio)

        if not eliminado:
            raise ValueError(
                "No se puede eliminar el socio porque tiene préstamos asociados."
            )

        return True