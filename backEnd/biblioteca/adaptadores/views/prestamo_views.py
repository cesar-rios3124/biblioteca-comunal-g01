
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers

from biblioteca.infrastructure.repositories.prestamo_repository_oracle import (
    PrestamoRepositoryOracle,
)
from biblioteca.infrastructure.repositories.socio_repository_oracle import (
    SocioRepositoryOracle,
)
from biblioteca.infrastructure.repositories.detalle_prestamo_repository_oracle import (
    DetallePrestamoRepositoryOracle,
)
from biblioteca.infrastructure.repositories.libro_repository_oracle import (
    LibroRepositoryOracle,
)

from biblioteca.adaptadores.serializers.prestamo_serializer import (
    PrestamoSerializer,
)
from biblioteca.adaptadores.serializers.detalle_prestamo_serializer import (
    DetallePrestamoSerializer,
)

from biblioteca.application.use_cases.crear_prestamo import CrearPrestamo
from biblioteca.application.use_cases.listar_prestamos import ListarPrestamos
from biblioteca.application.use_cases.actualizar_prestamo import ActualizarPrestamo
from biblioteca.application.use_cases.eliminar_prestamo import EliminarPrestamo
from biblioteca.application.use_cases.devolver_prestamo import DevolverPrestamo

from biblioteca.application.exceptions import (
    SocioNoEncontradoError,
    SocioInactivoError,
    SocioConPrestamoAtrasadoError,
    PrestamoNoEncontradoError,
    LibroNoEncontradoError,
    EjemplaresInsuficientesError,
    EstadoPrestamoInvalidoError,
    LimiteLibrosExcedidoError,
)


@api_view(["GET", "POST"])
def prestamos(request):
    prestamo_repo = PrestamoRepositoryOracle()
    socio_repo = SocioRepositoryOracle()
    detalle_repo = DetallePrestamoRepositoryOracle()
    libro_repo = LibroRepositoryOracle()

    if request.method == "GET":
        resultado = ListarPrestamos(prestamo_repo).ejecutar()
        return Response(PrestamoSerializer(resultado, many=True).data)

    id_socio = request.data.get("id_socio")
    detalles = request.data.get("detalles")

    try:
        id_socio = serializers.IntegerField().run_validation(id_socio)
    except serializers.ValidationError as error:
        return Response(
            {"id_socio": error.detail},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not isinstance(detalles, list) or not detalles:
        return Response(
            {"error": "Debe incluir al menos un libro en el préstamo."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = DetallePrestamoSerializer(data=detalles, many=True)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        resultado = CrearPrestamo(
            prestamo_repo,
            socio_repo,
            detalle_repo,
            libro_repo,
        ).ejecutar(
            id_socio=id_socio,
            detalles=[
                (detalle["id_libro"], detalle["cantidad"])
                for detalle in serializer.validated_data
            ],
        )

        return Response(
            PrestamoSerializer(resultado).data,
            status=status.HTTP_201_CREATED,
        )

    except SocioNoEncontradoError as error:
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
        SocioInactivoError,
        SocioConPrestamoAtrasadoError,
        EjemplaresInsuficientesError,
        LimiteLibrosExcedidoError,
        EstadoPrestamoInvalidoError,
        ValueError,
    ) as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "DELETE"])
def prestamo_detalle(request, id_prestamo):
    prestamo_repo = PrestamoRepositoryOracle()
    detalle_repo = DetallePrestamoRepositoryOracle()

    if request.method == "GET":
        prestamo = prestamo_repo.obtener_por_id(id_prestamo)

        if prestamo is None:
            return Response(
                {"error": "El préstamo no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )

        detalles = detalle_repo.listar_por_prestamo(id_prestamo)

        return Response({
            **PrestamoSerializer(prestamo).data,
            "detalles": DetallePrestamoSerializer(
                detalles,
                many=True,
            ).data,
        })

    if request.method == "PUT":
        fecha = request.data.get("fecha_devolucion_esperada")

        if not fecha:
            return Response(
                {"error": "Debe indicar la fecha de devolución esperada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            fecha_validada = serializers.DateTimeField().run_validation(fecha)
        except serializers.ValidationError as error:
            return Response(
                {"fecha_devolucion_esperada": error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            resultado = ActualizarPrestamo(prestamo_repo).ejecutar(
                id_prestamo,
                fecha_validada,
            )

            return Response(PrestamoSerializer(resultado).data)

        except PrestamoNoEncontradoError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except EstadoPrestamoInvalidoError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_409_CONFLICT,
            )

    try:
        EliminarPrestamo(
            prestamo_repo,
            detalle_repo,
        ).ejecutar(id_prestamo)

        return Response(status=status.HTTP_204_NO_CONTENT)

    except PrestamoNoEncontradoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_404_NOT_FOUND,
        )

    except ValueError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_409_CONFLICT,
        )


@api_view(["POST"])
def devolver_prestamo(request, id_prestamo):
    prestamo_repo = PrestamoRepositoryOracle()
    detalle_repo = DetallePrestamoRepositoryOracle()
    libro_repo = LibroRepositoryOracle()

    try:
        resultado = DevolverPrestamo(
            prestamo_repo,
            detalle_repo,
            libro_repo,
        ).ejecutar(id_prestamo)

        return Response(PrestamoSerializer(resultado).data)

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

    except EstadoPrestamoInvalidoError as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_409_CONFLICT,
        )
