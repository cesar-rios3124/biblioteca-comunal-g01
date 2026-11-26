from rest_framework import serializers


class GeneroSerializer(serializers.Serializer):
    id_genero = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)