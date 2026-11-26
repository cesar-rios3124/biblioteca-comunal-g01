
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission

from biblioteca.infrastructure.repositories.socio_repository_oracle import (
    SocioRepositoryOracle,
)
from biblioteca.adaptadores.serializers.socio_serializer import SocioSerializer

from biblioteca.application.use_cases.crear_socio import CrearSocio
from biblioteca.application.use_cases.listar_socios import ListarSocios
from biblioteca.application.use_cases.actualizar_socio import ActualizarSocio
from biblioteca.application.use_cases.eliminar_socio import EliminarSocio

from biblioteca.application.exceptions import (
    RutDuplicadoError,
    SocioNoEncontradoError,
)


class EsAdministradorBiblioteca(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.groups.filter(
                    name="Administrador de Biblioteca"
                ).exists()
            )
        )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def socios(request):
    repositorio = SocioRepositoryOracle()

    if request.method == "GET":
        resultado = ListarSocios(repositorio).ejecutar()
        return Response(SocioSerializer(resultado, many=True).data)

    permiso = EsAdministradorBiblioteca()
    if not permiso.has_permission(request, None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = SocioSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    datos = serializer.validated_data.copy()
    datos.pop("activo", None)

    try:
        resultado = CrearSocio(repositorio).ejecutar(**datos)
        return Response(
            SocioSerializer(resultado).data,
            status=status.HTTP_201_CREATED
        )
    except RutDuplicadoError as error:
        return Response({"error": str(error)}, status=status.HTTP_409_CONFLICT)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def socio_detalle(request, id_socio):
    repositorio = SocioRepositoryOracle()

    if request.method == "GET":
        socio = repositorio.obtener_por_id(id_socio)
        if socio is None:
            return Response(
                {"error": "Socio no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(SocioSerializer(socio).data)

    permiso = EsAdministradorBiblioteca()
    if not permiso.has_permission(request, None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "PUT":
        serializer = SocioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data.copy()
        datos.pop("id_socio", None)

        try:
            resultado = ActualizarSocio(repositorio).ejecutar(
                id_socio=id_socio,
                **datos
            )
            if resultado is None:
                return Response(
                    {"error": "No se pudo actualizar el socio."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(SocioSerializer(resultado).data)

        except SocioNoEncontradoError as error:
            return Response({"error": str(error)}, status=status.HTTP_404_NOT_FOUND)
        except RutDuplicadoError as error:
            return Response({"error": str(error)}, status=status.HTTP_409_CONFLICT)

    try:
        EliminarSocio(repositorio).ejecutar(id_socio)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except SocioNoEncontradoError as error:
        return Response({"error": str(error)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as error:
        return Response({"error": str(error)}, status=status.HTTP_409_CONFLICT)
