from django.db import models


class GeneroModel(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = "GENEROS"

    def __str__(self):
        return self.nombre