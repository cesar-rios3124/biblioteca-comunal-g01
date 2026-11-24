
from django.contrib import admin
from django.urls import path

from biblioteca.adaptadores.views.autenticacion_views import (
    obtener_csrf,
    login,
    logout,
    me,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticación
    path("api/auth/csrf/", obtener_csrf, name="csrf"),
    path("api/auth/login/", login, name="login"),
    path("api/auth/logout/", logout, name="logout"),
    path("api/auth/me/", me, name="me"),
]
