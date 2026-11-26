
from django.contrib import admin
from django.urls import path

from biblioteca.adaptadores.views.autenticacion_views import (
    obtener_csrf,
    login,
    logout,
    me,
)

from biblioteca.adaptadores.views.socio_views import (
    socios,
    socio_detalle,
)

from biblioteca.adaptadores.views.genero_views import (
    generos,
    genero_detalle,
)

from biblioteca.adaptadores.views.libro_views import (
    libros,
    libro_detalle,
)

from biblioteca.adaptadores.views.prestamo_views import (
    prestamos,
    prestamo_detalle,
    devolver_prestamo,
)

from biblioteca.adaptadores.views.detalle_prestamo_views import (
    detalles_prestamo,
    detalle_prestamo,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticación
    path("api/auth/csrf/", obtener_csrf, name="csrf"),
    path("api/auth/login/", login, name="login"),
    path("api/auth/logout/", logout, name="logout"),
    path("api/auth/me/", me, name="me"),

    # CRUD de socios
    path("api/socios/", socios, name="socios"),
    path("api/socios/<int:id_socio>/", socio_detalle, name="socio_detalle"),

    # CRUD de géneros
    path("api/generos/", generos, name="generos"),
    path("api/generos/<int:id_genero>/", genero_detalle, name="genero_detalle"),

    # CRUD de libros
    path("api/libros/", libros, name="libros"),
    path("api/libros/<int:id_libro>/", libro_detalle, name="libro_detalle"),

    # CRUD de préstamos
    path("api/prestamos/", prestamos, name="prestamos"),
    path("api/prestamos/<int:id_prestamo>/", prestamo_detalle, name="prestamo_detalle"),
    path("api/prestamos/<int:id_prestamo>/devolver/", devolver_prestamo, name="devolver_prestamo"),

    # CRUD de detalles de préstamos
    path("api/prestamos/<int:id_prestamo>/detalles/", detalles_prestamo, name="detalles_prestamo"),
    path("api/prestamos/<int:id_prestamo>/detalles/<int:id_libro>/", detalle_prestamo, name="detalle_prestamo"),
]
