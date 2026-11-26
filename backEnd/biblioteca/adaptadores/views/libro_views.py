
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission

from biblioteca.infrastructure.repositories.libro_repository_oracle import (
    LibroRepositoryOracle,
)

from biblioteca.adaptadores.serializers.libro_serializer import (
    LibroSerializer,
)

from biblioteca.application.use_cases.crear_libro import CrearLibro
from biblioteca.application.use_cases.listar_libros import ListarLibros
from biblioteca.application.use_cases.actualizar_libro import ActualizarLibro
from biblioteca.application.use_cases.eliminar_libro import EliminarLibro

from biblioteca.application.exceptions import (
    LibroNoEncontradoError,
    IsbnDuplicadoError,
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
def libros(request):
    repositorio = LibroRepositoryOracle()

    if request.method == "GET":
        resultado = ListarLibros(repositorio).ejecutar()
        return Response(LibroSerializer(resultado, many=True).data)

    if not EsAdministradorBiblioteca().has_permission(request, None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = LibroSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        resultado = CrearLibro(repositorio).ejecutar(
            **serializer.validated_data
        )

        return Response(
            LibroSerializer(resultado).data,
            status=status.HTTP_201_CREATED,
        )

    except IsbnDuplicadoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_409_CONFLICT,
        )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def libro_detalle(request, id_libro):
    repositorio = LibroRepositoryOracle()

    if request.method == "GET":
        libro = repositorio.obtener_por_id(id_libro)

        if libro is None:
            return Response(
                {"error": "El libro no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(LibroSerializer(libro).data)

    if not EsAdministradorBiblioteca().has_permission(request, None):
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "PUT":
        serializer = LibroSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        datos = serializer.validated_data.copy()

        try:
            resultado = ActualizarLibro(repositorio).ejecutar(
                id_libro=id_libro,
                **datos,
            )

            if resultado is None:
                return Response(
                    {"error": "El libro no existe."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(LibroSerializer(resultado).data)

        except LibroNoEncontradoError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except IsbnDuplicadoError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_409_CONFLICT,
            )

    try:
        EliminarLibro(repositorio).ejecutar(id_libro)
        return Response(status=status.HTTP_204_NO_CONTENT)

    except LibroNoEncontradoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_404_NOT_FOUND,
        )

    except ValueError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_409_CONFLICT,
        )
