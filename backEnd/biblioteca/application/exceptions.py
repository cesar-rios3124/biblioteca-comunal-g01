"""
Excepciones propias de la biblioteca.
Agrupan los errores de negocio sin depender de Django ni de HTTP.
"""


class NoEncontradoError(Exception):
    """El registro solicitado no existe."""


class DuplicadoError(Exception):
    """Un dato que debe ser único ya está registrado."""


class ReglaNegocioError(Exception):
    """La operación incumple una regla del negocio."""


# Socios
class SocioNoEncontradoError(NoEncontradoError):
    pass


class RutDuplicadoError(DuplicadoError):
    pass


# Géneros
class GeneroNoEncontradoError(NoEncontradoError):
    pass


class GeneroDuplicadoError(DuplicadoError):
    pass


# Libros
class LibroNoEncontradoError(NoEncontradoError):
    pass


class IsbnDuplicadoError(DuplicadoError):
    pass


# Préstamos
class PrestamoNoEncontradoError(NoEncontradoError):
    pass


# Detalles de préstamos
class DetallePrestamoNoEncontradoError(NoEncontradoError):
    pass


# Reglas de negocio
class SocioInactivoError(ReglaNegocioError):
    pass


class SocioConPrestamoAtrasadoError(ReglaNegocioError):
    pass


class EjemplaresInsuficientesError(ReglaNegocioError):
    pass


class LimiteLibrosExcedidoError(ReglaNegocioError):
    pass


class EstadoPrestamoInvalidoError(ReglaNegocioError):
    pass