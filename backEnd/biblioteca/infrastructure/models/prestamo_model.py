from django.db import models


class PrestamoModel(models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    id_socio = models.IntegerField()
    fecha_prestamo = models.DateTimeField()
    fecha_devolucion_esperada = models.DateTimeField()
    estado = models.CharField(max_length=10, default="activo")

    class Meta:
        managed = False
        db_table = "PRESTAMOS"

    def __str__(self):
        return str(self.id_prestamo)