
from django.db import connections

from biblioteca.domain.entities import Prestamo
from biblioteca.domain.repositories.prestamo_repository import PrestamoRepository


class PrestamoRepositoryOracle(PrestamoRepository):

    def guardar(self, prestamo: Prestamo) -> Prestamo:
        with connections["negocio"].cursor() as cursor:
            id_prestamo = cursor.var(int)

            cursor.execute(
                """
                INSERT INTO PRESTAMOS (
                    ID_SOCIO,
                    FECHA_PRESTAMO,
                    FECHA_DEVOLUCION_ESPERADA,
                    ESTADO
                )
                VALUES (%s, %s, %s, %s)
                RETURNING ID_PRESTAMO INTO %s
                """,
                [
                    prestamo.id_socio,
                    prestamo.fecha_prestamo,
                    prestamo.fecha_devolucion_esperada,
                    prestamo.estado,
                    id_prestamo,
                ],
            )

            valor_id = id_prestamo.getvalue()
            prestamo.id_prestamo = (
                valor_id[0] if isinstance(valor_id, list) else valor_id
            )

        return prestamo

    def obtener_por_id(self, id_prestamo: int):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_PRESTAMO, ID_SOCIO, FECHA_PRESTAMO,
                       FECHA_DEVOLUCION_ESPERADA, ESTADO
                FROM PRESTAMOS
                WHERE ID_PRESTAMO = %s
                """,
                [id_prestamo],
            )
            fila = cursor.fetchone()

        if fila is None:
            return None

        return Prestamo(
            id_socio=fila[1],
            fecha_prestamo=fila[2],
            fecha_devolucion_esperada=fila[3],
            estado=fila[4],
            id_prestamo=fila[0],
        )

    def listar(self):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_PRESTAMO, ID_SOCIO, FECHA_PRESTAMO,
                       FECHA_DEVOLUCION_ESPERADA, ESTADO
                FROM PRESTAMOS
                ORDER BY ID_PRESTAMO
                """
            )
            filas = cursor.fetchall()

        return [
            Prestamo(
                id_socio=fila[1],
                fecha_prestamo=fila[2],
                fecha_devolucion_esperada=fila[3],
                estado=fila[4],
                id_prestamo=fila[0],
            )
            for fila in filas
        ]

    def listar_por_socio(self, id_socio: int):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_PRESTAMO, ID_SOCIO, FECHA_PRESTAMO,
                       FECHA_DEVOLUCION_ESPERADA, ESTADO
                FROM PRESTAMOS
                WHERE ID_SOCIO = %s
                ORDER BY ID_PRESTAMO
                """,
                [id_socio],
            )
            filas = cursor.fetchall()

        return [
            Prestamo(
                id_socio=fila[1],
                fecha_prestamo=fila[2],
                fecha_devolucion_esperada=fila[3],
                estado=fila[4],
                id_prestamo=fila[0],
            )
            for fila in filas
        ]

    def actualizar(self, prestamo: Prestamo):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                UPDATE PRESTAMOS
                SET ID_SOCIO = %s,
                    FECHA_PRESTAMO = %s,
                    FECHA_DEVOLUCION_ESPERADA = %s,
                    ESTADO = %s
                WHERE ID_PRESTAMO = %s
                """,
                [
                    prestamo.id_socio,
                    prestamo.fecha_prestamo,
                    prestamo.fecha_devolucion_esperada,
                    prestamo.estado,
                    prestamo.id_prestamo,
                ],
            )

            if cursor.rowcount == 0:
                return None

        return prestamo

    def marcar_atrasados(self) -> int:
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                UPDATE PRESTAMOS
                SET ESTADO = 'atrasado'
                WHERE ESTADO = 'activo'
                  AND FECHA_DEVOLUCION_ESPERADA <
                      CAST(SYS_EXTRACT_UTC(SYSTIMESTAMP) AS TIMESTAMP)
                """
            )

            return cursor.rowcount

    def eliminar(self, id_prestamo: int) -> bool:
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM PRESTAMOS
                WHERE ID_PRESTAMO = %s
                """,
                [id_prestamo],
            )

            return cursor.rowcount > 0
