from rest_framework import serializers


class SocioSerializer(serializers.Serializer):
    id_socio = serializers.IntegerField(read_only=True)
    rut = serializers.CharField(max_length=12)
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    telefono = serializers.CharField(max_length=20)
    activo = serializers.BooleanField()