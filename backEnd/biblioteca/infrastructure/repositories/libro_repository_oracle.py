
from django.db import connections

from biblioteca.domain.entities import Libro
from biblioteca.domain.repositories.libro_repository import LibroRepository


class LibroRepositoryOracle(LibroRepository):

    def guardar(self, libro: Libro) -> Libro:
        with connections["negocio"].cursor() as cursor:
            id_libro = cursor.var(int)

            cursor.execute(
                """
                INSERT INTO LIBROS (
                    ISBN, TITULO, AUTOR, ANIO,
                    ID_GENERO, EJEMPLARES_DISPONIBLES
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING ID_LIBRO INTO %s
                """,
                [
                    libro.isbn,
                    libro.titulo,
                    libro.autor,
                    libro.anio,
                    libro.id_genero,
                    libro.ejemplares_disponibles,
                    id_libro,
                ],
            )

            valor_id = id_libro.getvalue()
            libro.id_libro = (
                valor_id[0] if isinstance(valor_id, list) else valor_id
            )

        return libro

    def obtener_por_id(self, id_libro: int):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_LIBRO, ISBN, TITULO, AUTOR, ANIO,
                       ID_GENERO, EJEMPLARES_DISPONIBLES
                FROM LIBROS
                WHERE ID_LIBRO = %s
                """,
                [id_libro],
            )
            fila = cursor.fetchone()

        if fila is None:
            return None

        return Libro(
            isbn=fila[1],
            titulo=fila[2],
            autor=fila[3],
            anio=fila[4],
            id_genero=fila[5],
            ejemplares_disponibles=fila[6],
            id_libro=fila[0],
        )

    def obtener_por_isbn(self, isbn: str):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_LIBRO, ISBN, TITULO, AUTOR, ANIO,
                       ID_GENERO, EJEMPLARES_DISPONIBLES
                FROM LIBROS
                WHERE ISBN = %s
                """,
                [isbn],
            )
            fila = cursor.fetchone()

        if fila is None:
            return None

        return Libro(
            isbn=fila[1],
            titulo=fila[2],
            autor=fila[3],
            anio=fila[4],
            id_genero=fila[5],
            ejemplares_disponibles=fila[6],
            id_libro=fila[0],
        )

    def listar(self):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_LIBRO, ISBN, TITULO, AUTOR, ANIO,
                       ID_GENERO, EJEMPLARES_DISPONIBLES
                FROM LIBROS
                ORDER BY ID_LIBRO
                """
            )
            filas = cursor.fetchall()

        return [
            Libro(
                isbn=fila[1],
                titulo=fila[2],
                autor=fila[3],
                anio=fila[4],
                id_genero=fila[5],
                ejemplares_disponibles=fila[6],
                id_libro=fila[0],
            )
            for fila in filas
        ]

    def actualizar(self, libro: Libro):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                UPDATE LIBROS
                SET ISBN = %s,
                    TITULO = %s,
                    AUTOR = %s,
                    ANIO = %s,
                    ID_GENERO = %s,
                    EJEMPLARES_DISPONIBLES = %s
                WHERE ID_LIBRO = %s
                """,
                [
                    libro.isbn,
                    libro.titulo,
                    libro.autor,
                    libro.anio,
                    libro.id_genero,
                    libro.ejemplares_disponibles,
                    libro.id_libro,
                ],
            )

            if cursor.rowcount == 0:
                return None

        return libro

    def eliminar(self, id_libro: int) -> bool:
        with connections["negocio"].cursor() as cursor:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM DETALLE_PRESTAMO
                WHERE ID_LIBRO = %s
                """,
                [id_libro],
            )

            cantidad_detalles = cursor.fetchone()[0]

            if cantidad_detalles > 0:
                return False

            cursor.execute(
                """
                DELETE FROM LIBROS
                WHERE ID_LIBRO = %s
                """,
                [id_libro],
            )

            return cursor.rowcount > 0
