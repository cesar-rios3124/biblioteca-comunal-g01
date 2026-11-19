"""
Entidad Genero.
Representa un género literario de la biblioteca.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Genero:
    nombre: str
    id_genero: Optional[int] = None