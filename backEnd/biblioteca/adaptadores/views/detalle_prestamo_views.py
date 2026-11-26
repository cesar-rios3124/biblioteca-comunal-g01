
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from biblioteca.infrastructure.repositories.prestamo_repository_oracle import (
    PrestamoRepositoryOracle,
)
from biblioteca.infrastructure.repositories.detalle_prestamo_repository_oracle import (
    DetallePrestamoRepositoryOracle,
)
from biblioteca.infrastructure.repositories.libro_repository_oracle import (
    LibroRepositoryOracle,
)

from biblioteca.adaptadores.serializers.detalle_prestamo_serializer import (
    DetallePrestamoSerializer,
)

from biblioteca.application.use_cases.crear_detalle_prestamo import (
    CrearDetallePrestamo,
)
from biblioteca.application.use_cases.listar_detalles_prestamo import (
    ListarDetallesPrestamo,
)
from biblioteca.application.use_cases.actualizar_detalle_prestamo import (
    ActualizarDetallePrestamo,
)
from biblioteca.application.use_cases.eliminar_detalle_prestamo import (
    EliminarDetallePrestamo,
)

from biblioteca.application.exceptions import (
    PrestamoNoEncontradoError,
    LibroNoEncontradoError,
    DetallePrestamoNoEncontradoError,
    EstadoPrestamoInvalidoError,
    EjemplaresInsuficientesError,
    LimiteLibrosExcedidoError,
)


@api_view(["GET", "POST"])
def detalles_prestamo(request, id_prestamo):
    prestamo_repo = PrestamoRepositoryOracle()
    detalle_repo = DetallePrestamoRepositoryOracle()
    libro_repo = LibroRepositoryOracle()

    if request.method == "GET":
        resultado = ListarDetallesPrestamo(
            detalle_repo
        ).ejecutar(id_prestamo)

        return Response(
            DetallePrestamoSerializer(resultado, many=True).data
        )

    serializer = DetallePrestamoSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    datos = serializer.validated_data

    try:
        resultado = CrearDetallePrestamo(
            detalle_repo,
            prestamo_repo,
            libro_repo,
        ).ejecutar(
            id_prestamo=id_prestamo,
            id_libro=datos["id_libro"],
            cantidad=datos["cantidad"],
        )

        return Response(
            DetallePrestamoSerializer(resultado).data,
            status=status.HTTP_201_CREATED,
        )

    except PrestamoNoEncontradoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_404_NOT_FOUND,
        )

    except LibroNoEncontradoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_404_NOT_FOUND,
        )

    except (
        EstadoPrestamoInvalidoError,
        EjemplaresInsuficientesError,
        LimiteLibrosExcedidoError,
        ValueError,
    ) as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PUT", "DELETE"])
def detalle_prestamo(request, id_prestamo, id_libro):
    detalle_repo = DetallePrestamoRepositoryOracle()
    prestamo_repo = PrestamoRepositoryOracle()
    libro_repo = LibroRepositoryOracle()

    if request.method == "PUT":
        serializer = DetallePrestamoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        cantidad = serializer.validated_data["cantidad"]

        try:
            resultado = ActualizarDetallePrestamo(
                detalle_repo,
                prestamo_repo,
                libro_repo,
            ).ejecutar(
                id_prestamo=id_prestamo,
                id_libro=id_libro,
                nueva_cantidad=cantidad,
            )

            return Response(DetallePrestamoSerializer(resultado).data)

        except (
            PrestamoNoEncontradoError,
            LibroNoEncontradoError,
            DetallePrestamoNoEncontradoError,
        ) as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (
            EstadoPrestamoInvalidoError,
            EjemplaresInsuficientesError,
            LimiteLibrosExcedidoError,
            ValueError,
        ) as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    try:
        EliminarDetallePrestamo(
            detalle_repo,
            prestamo_repo,
            libro_repo,
        ).ejecutar(id_prestamo, id_libro)

        return Response(status=status.HTTP_204_NO_CONTENT)

    except (
        PrestamoNoEncontradoError,
        LibroNoEncontradoError,
        DetallePrestamoNoEncontradoError,
    ) as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_404_NOT_FOUND,
        )

    except EstadoPrestamoInvalidoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_409_CONFLICT,
        )
