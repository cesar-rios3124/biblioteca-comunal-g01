
from django.db import connections

from biblioteca.domain.entities import DetallePrestamo
from biblioteca.domain.repositories.detalle_prestamo_repository import (
    DetallePrestamoRepository,
)


class DetallePrestamoRepositoryOracle(DetallePrestamoRepository):

    def guardar(self, detalle: DetallePrestamo) -> DetallePrestamo:
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO DETALLE_PRESTAMO (
                    ID_PRESTAMO,
                    ID_LIBRO,
                    CANTIDAD
                )
                VALUES (%s, %s, %s)
                """,
                [
                    detalle.id_prestamo,
                    detalle.id_libro,
                    detalle.cantidad,
                ],
            )
        return detalle

    def obtener_por_id(
        self, id_prestamo: int, id_libro: int
    ):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_PRESTAMO, ID_LIBRO, CANTIDAD
                FROM DETALLE_PRESTAMO
                WHERE ID_PRESTAMO = %s AND ID_LIBRO = %s
                """,
                [id_prestamo, id_libro],
            )
            fila = cursor.fetchone()

        if fila is None:
            return None

        return DetallePrestamo(
            id_prestamo=fila[0],
            id_libro=fila[1],
            cantidad=fila[2],
        )

    def listar_por_prestamo(self, id_prestamo: int):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                SELECT ID_PRESTAMO, ID_LIBRO, CANTIDAD
                FROM DETALLE_PRESTAMO
                WHERE ID_PRESTAMO = %s
                ORDER BY ID_LIBRO
                """,
                [id_prestamo],
            )
            filas = cursor.fetchall()

        return [
            DetallePrestamo(
                id_prestamo=fila[0],
                id_libro=fila[1],
                cantidad=fila[2],
            )
            for fila in filas
        ]

    def actualizar(self, detalle: DetallePrestamo):
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                UPDATE DETALLE_PRESTAMO
                SET CANTIDAD = %s
                WHERE ID_PRESTAMO = %s AND ID_LIBRO = %s
                """,
                [
                    detalle.cantidad,
                    detalle.id_prestamo,
                    detalle.id_libro,
                ],
            )

            if cursor.rowcount == 0:
                return None

        return detalle

    def eliminar(self, id_prestamo: int, id_libro: int) -> bool:
        with connections["negocio"].cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM DETALLE_PRESTAMO
                WHERE ID_PRESTAMO = %s AND ID_LIBRO = %s
                """,
                [id_prestamo, id_libro],
            )
            return cursor.rowcount > 0
