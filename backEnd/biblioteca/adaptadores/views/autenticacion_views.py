
import json

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@require_GET
@ensure_csrf_cookie
def obtener_csrf(request):
    return JsonResponse({
        "csrfToken": get_token(request)
    })


@require_POST
@csrf_protect
def login(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Los datos enviados no son válidos."},
            status=400
        )

    usuario = authenticate(
        request,
        username=datos.get("username"),
        password=datos.get("password")
    )

    if usuario is None:
        return JsonResponse(
            {"error": "Usuario o contraseña incorrectos."},
            status=401
        )

    token, _ = Token.objects.get_or_create(user=usuario)

    respuesta = JsonResponse({
        "mensaje": "Inicio de sesión exitoso.",
        "usuario": usuario.username
    })

    cookie = settings.AUTH_COOKIE

    respuesta.set_cookie(
        key=cookie["NAME"],
        value=token.key,
        max_age=cookie["MAX_AGE"],
        path=cookie["PATH"],
        httponly=True,
        secure=cookie["SECURE"],
        samesite=cookie["SAMESITE"]
    )

    return respuesta


@require_POST
@csrf_protect
def logout(request):
    token_key = request.COOKIES.get(
        settings.AUTH_COOKIE["NAME"]
    )

    if token_key:
        Token.objects.filter(key=token_key).delete()

    respuesta = JsonResponse({
        "mensaje": "Sesión cerrada correctamente."
    })

    respuesta.delete_cookie(
        key=settings.AUTH_COOKIE["NAME"],
        path=settings.AUTH_COOKIE["PATH"],
        samesite=settings.AUTH_COOKIE["SAMESITE"]
    )

    return respuesta


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return JsonResponse({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
        "autenticado": True
    })
