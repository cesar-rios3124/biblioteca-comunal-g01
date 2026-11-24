
from django.contrib import admin
from django.db import connections
from django.http import HttpResponse
from django.urls import path
from django.utils.html import escape
from django.core.exceptions import PermissionDenied

from biblioteca.infrastructure.models.socio_model import SocioModel
from biblioteca.infrastructure.models.genero_model import GeneroModel
from biblioteca.infrastructure.models.libro_model import LibroModel
from biblioteca.infrastructure.models.prestamo_model import PrestamoModel


@admin.register(SocioModel)
class SocioAdmin(admin.ModelAdmin):
    list_display = ("id_socio", "rut", "nombre", "email", "telefono", "activo")
    search_fields = ("rut", "nombre", "email")
    list_filter = ("activo",)


@admin.register(GeneroModel)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ("id_genero", "nombre")
    search_fields = ("nombre",)


@admin.register(LibroModel)
class LibroAdmin(admin.ModelAdmin):
    list_display = (
        "id_libro", "isbn", "titulo", "autor", "anio",
        "id_genero", "ejemplares_disponibles",
    )
    search_fields = ("isbn", "titulo", "autor")
    list_filter = ("id_genero", "anio")


@admin.register(PrestamoModel)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id_prestamo", "id_socio", "fecha_prestamo",
        "fecha_devolucion_esperada", "estado",
    )
    search_fields = ("id_prestamo", "id_socio")
    list_filter = ("estado", "fecha_prestamo")


def ver_detalles_prestamo(request):
    if not request.user.has_perm("biblioteca.view_detalleprestamomodel"):
        raise PermissionDenied

    with connections["negocio"].cursor() as cursor:
        cursor.execute("""
            SELECT ID_PRESTAMO, ID_LIBRO, CANTIDAD
            FROM DETALLE_PRESTAMO
            ORDER BY ID_PRESTAMO, ID_LIBRO
        """)
        filas = cursor.fetchall()

    encabezado = """
        <h1>Detalle de préstamos</h1>
        <table class="table">
        <thead>
            <tr>
                <th>ID préstamo</th>
                <th>ID libro</th>
                <th>Cantidad</th>
            </tr>
        </thead>
        <tbody>
    """

    contenido = "".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            escape(str(fila[0])),
            escape(str(fila[1])),
            escape(str(fila[2]))
        )
        for fila in filas
    )

    html = encabezado + contenido + """
        </tbody>
        </table>
        <p><a href="/admin/">Volver al administrador</a></p>
    """

    return HttpResponse(html)


urls_originales = admin.site.get_urls


def urls_personalizadas():
    urls = urls_originales()
    urls.insert(
        0,
        path(
            "biblioteca/detalles-prestamo/",
            admin.site.admin_view(ver_detalles_prestamo),
            name="detalle_prestamo",
        ),
    )
    return urls


admin.site.get_urls = urls_personalizadas


contexto_original = admin.site.each_context


def contexto_personalizado(request):
    contexto = contexto_original(request)

    if request.user.has_perm("biblioteca.view_detalleprestamomodel"):
        contexto["url_detalles_prestamo"] = (
            "/admin/biblioteca/detalles-prestamo/"
        )

    return contexto


admin.site.each_context = contexto_personalizado
