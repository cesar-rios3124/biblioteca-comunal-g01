
from rest_framework import serializers


class PrestamoSerializer(serializers.Serializer):
    id_prestamo = serializers.IntegerField(read_only=True)
    id_socio = serializers.IntegerField()
    fecha_prestamo = serializers.DateTimeField(read_only=True)
    fecha_devolucion_esperada = serializers.DateTimeField()
    estado = serializers.CharField(read_only=True)
