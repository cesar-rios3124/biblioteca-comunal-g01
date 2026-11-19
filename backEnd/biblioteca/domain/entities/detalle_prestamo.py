"""
Entidad DetallePrestamo.
Representa los libros y sus cantidades
asociados a un préstamo.
"""

from dataclasses import dataclass


@dataclass
class DetallePrestamo:
    id_prestamo: int
    id_libro: int
    cantidad: int