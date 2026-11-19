from django.db import models


class DetallePrestamoModel(models.Model):
    pk = models.CompositePrimaryKey("id_prestamo", "id_libro")

    id_prestamo = models.IntegerField()
    id_libro = models.IntegerField()
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = "DETALLE_PRESTAMO"