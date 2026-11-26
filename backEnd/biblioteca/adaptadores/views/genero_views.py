
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission

from biblioteca.infrastructure.repositories.genero_repository_oracle import (
    GeneroRepositoryOracle,
)

from biblioteca.adaptadores.serializers.genero_serializer import (
    GeneroSerializer,
)

from biblioteca.application.use_cases.crear_genero import CrearGenero
from biblioteca.application.use_cases.listar_generos import ListarGeneros
from biblioteca.application.use_cases.actualizar_genero import ActualizarGenero
from biblioteca.application.use_cases.eliminar_genero import EliminarGenero

from biblioteca.application.exceptions import (
    GeneroNoEncontradoError,
    GeneroDuplicadoError,
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
def generos(request):
    repositorio = GeneroRepositoryOracle()

    if request.method == "GET":
        resultado = ListarGeneros(repositorio).ejecutar()
        return Response(GeneroSerializer(resultado, many=True).data)

    if not EsAdministradorBiblioteca().has_permission(request, None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = GeneroSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        resultado = CrearGenero(repositorio).ejecutar(
            **serializer.validated_data
        )
        return Response(
            GeneroSerializer(resultado).data,
            status=status.HTTP_201_CREATED
        )
    except GeneroDuplicadoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_409_CONFLICT
        )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def genero_detalle(request, id_genero):
    repositorio = GeneroRepositoryOracle()

    if request.method == "GET":
        genero = repositorio.obtener_por_id(id_genero)

        if genero is None:
            return Response(
                {"error": "Género no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(GeneroSerializer(genero).data)

    if not EsAdministradorBiblioteca().has_permission(request, None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "PUT":
        serializer = GeneroSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            resultado = ActualizarGenero(repositorio).ejecutar(
                id_genero=id_genero,
                **serializer.validated_data
            )
            return Response(GeneroSerializer(resultado).data)

        except GeneroNoEncontradoError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_404_NOT_FOUND
            )
        except GeneroDuplicadoError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_409_CONFLICT
            )

    try:
        EliminarGenero(repositorio).ejecutar(id_genero)
        return Response(status=status.HTTP_204_NO_CONTENT)

    except GeneroNoEncontradoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_409_CONFLICT
        )
