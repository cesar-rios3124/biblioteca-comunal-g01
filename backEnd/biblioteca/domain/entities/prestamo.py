"""
Entidad Prestamo.
Representa un préstamo realizado por un socio
de la biblioteca comunal.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Prestamo:
    id_socio: int
    fecha_devolucion_esperada: datetime
    fecha_prestamo: Optional[datetime] = None
    estado: str = "activo"
    id_prestamo: Optional[int] = None