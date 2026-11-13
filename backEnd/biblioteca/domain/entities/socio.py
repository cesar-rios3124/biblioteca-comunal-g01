
"""
Entidad Socio.
Representa a un socio de la biblioteca comunal.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Socio:
    rut: str
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: bool = True
    id_socio: Optional[int] = None
