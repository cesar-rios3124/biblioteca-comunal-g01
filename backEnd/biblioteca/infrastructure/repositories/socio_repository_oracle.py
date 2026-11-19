
from django.db import connections

from biblioteca.domain.entities import Socio
from biblioteca.domain.repositories.socio_repository import SocioRepository


class SocioRepositoryOracle(SocioRepository):

    def guardar(self, socio: Socio) -> Socio:
        with connections["negocio"].cursor() as cursor:
            id_socio = cursor.var(int)

            cursor.execute(
                """
                INSERT INTO SOCIOS (
                    RUT, NOMBRE, EMAIL, TELEFONO, ACTIVO
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING ID_SOCIO INTO %s
                """,
                [
                    socio.rut,
                    socio.nombre,
                    socio.email,
                    socio.telefono,
                    1 if socio.activo else 0,
                    id_socio,
                ],
            )

            valor_id = id_socio.getvalue()
            socio.id_socio = valor_id[0] if isinstance(valor_id, list) else valor_id

        return socio

    def obtener_por_id(self, id_socio: int):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_SOCIO, RUT, NOMBRE, EMAIL, TELEFONO, ACTIVO
                FROM SOCIOS
                WHERE ID_SOCIO = %s
                """,
                [id_socio],
            )
            fila = cursor.fetchone()

        if fila is None:
            return None

        return Socio(
            rut=fila[1],
            nombre=fila[2],
            email=fila[3],
            telefono=fila[4],
            activo=bool(fila[5]),
            id_socio=fila[0],
        )

    def obtener_por_rut(self, rut: str):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_SOCIO, RUT, NOMBRE, EMAIL, TELEFONO, ACTIVO
                FROM SOCIOS
                WHERE RUT = %s
                """,
                [rut],
            )
            fila = cursor.fetchone()

        if fila is None:
            return None

        return Socio(
            rut=fila[1],
            nombre=fila[2],
            email=fila[3],
            telefono=fila[4],
            activo=bool(fila[5]),
            id_socio=fila[0],
        )

    def listar(self):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_SOCIO, RUT, NOMBRE, EMAIL, TELEFONO, ACTIVO
                FROM SOCIOS
                ORDER BY ID_SOCIO
                """
            )
            filas = cursor.fetchall()

        return [
            Socio(
                rut=fila[1],
                nombre=fila[2],
                email=fila[3],
                telefono=fila[4],
                activo=bool(fila[5]),
                id_socio=fila[0],
            )
            for fila in filas
        ]

    def actualizar(self, socio: Socio) -> Socio:
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                UPDATE SOCIOS
                SET RUT = %s,
                    NOMBRE = %s,
                    EMAIL = %s,
                    TELEFONO = %s,
                    ACTIVO = %s
                WHERE ID_SOCIO = %s
                """,
                [
                    socio.rut,
                    socio.nombre,
                    socio.email,
                    socio.telefono,
                    1 if socio.activo else 0,
                    socio.id_socio,
                ],
            )

            if cursor.rowcount == 0:
                return None

        return socio

    def eliminar(self, id_socio: int) -> bool:
        with connections["negocio"].cursor() as cursor:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM PRESTAMOS
                WHERE ID_SOCIO = %s
                """,
                [id_socio],
            )

            cantidad_prestamos = cursor.fetchone()[0]

            if cantidad_prestamos > 0:
                return False

            cursor.execute(
                """
                DELETE FROM SOCIOS
                WHERE ID_SOCIO = %s
                """,
                [id_socio],
            )

            return cursor.rowcount > 0
