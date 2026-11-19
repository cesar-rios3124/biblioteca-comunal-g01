
"""
Entidad Libro.
Representa un libro disponible en la biblioteca comunal.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Libro:
    isbn: str
    titulo: str
    autor: str
    anio: int
    id_genero: int
    ejemplares_disponibles: int = 0
    id_libro: Optional[int] = None
