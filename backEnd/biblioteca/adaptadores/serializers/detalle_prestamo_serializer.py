
from rest_framework import serializers


class DetallePrestamoSerializer(serializers.Serializer):
    id_prestamo = serializers.IntegerField(read_only=True)
    id_libro = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)
