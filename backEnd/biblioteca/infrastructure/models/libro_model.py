from django.db import models


class LibroModel(models.Model):
    id_libro = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    anio = models.IntegerField()
    id_genero = models.IntegerField()
    ejemplares_disponibles = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "LIBROS"

    def __str__(self):
        return self.titulo