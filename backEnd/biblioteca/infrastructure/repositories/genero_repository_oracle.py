
from django.db import connections

from biblioteca.domain.entities import Genero
from biblioteca.domain.repositories.genero_repository import GeneroRepository


class GeneroRepositoryOracle(GeneroRepository):

    def guardar(self, genero: Genero) -> Genero:
        with connections["negocio"].cursor() as cursor:
            id_genero = cursor.var(int)

            cursor.execute(
                """
                INSERT INTO GENEROS (NOMBRE)
                VALUES (%s)
                RETURNING ID_GENERO INTO %s
                """,
                [genero.nombre, id_genero],
            )

            valor_id = id_genero.getvalue()
            genero.id_genero = (
                valor_id[0] if isinstance(valor_id, list) else valor_id
            )

        return genero

    def obtener_por_id(self, id_genero: int):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_GENERO, NOMBRE
                FROM GENEROS
                WHERE ID_GENERO = %s
                """,
                [id_genero],
            )
            fila = cursor.fetchone()

        if fila is None:
            return None

        return Genero(
            nombre=fila[1],
            id_genero=fila[0],
        )

    def listar(self):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_GENERO, NOMBRE
                FROM GENEROS
                ORDER BY ID_GENERO
                """
            )
            filas = cursor.fetchall()

        return [
            Genero(nombre=fila[1], id_genero=fila[0])
            for fila in filas
        ]

    def actualizar(self, genero: Genero):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                UPDATE GENEROS
                SET NOMBRE = %s
                WHERE ID_GENERO = %s
                """,
                [genero.nombre, genero.id_genero],
            )

            if cursor.rowcount == 0:
                return None

        return genero

    def eliminar(self, id_genero: int) -> bool:
        with connections["negocio"].cursor() as cursor:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM LIBROS
                WHERE ID_GENERO = %s
                """,
                [id_genero],
            )

            cantidad_libros = cursor.fetchone()[0]

            if cantidad_libros > 0:
                return False

            cursor.execute(
                """
                DELETE FROM GENEROS
                WHERE ID_GENERO = %s
                """,
                [id_genero],
            )

            return cursor.rowcount > 0
