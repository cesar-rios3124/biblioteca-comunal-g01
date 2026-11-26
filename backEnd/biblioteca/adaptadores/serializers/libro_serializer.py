from rest_framework import serializers


class LibroSerializer(serializers.Serializer):
    id_libro = serializers.IntegerField(read_only=True)
    isbn = serializers.CharField(max_length=20)
    titulo = serializers.CharField(max_length=200)
    autor = serializers.CharField(max_length=150)
    anio = serializers.IntegerField()
    id_genero = serializers.IntegerField()
    ejemplares_disponibles = serializers.IntegerField(min_value=0)