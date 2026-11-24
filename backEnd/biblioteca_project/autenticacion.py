
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.middleware.csrf import CsrfViewMiddleware


class CookieTokenAuthentication(TokenAuthentication):
    """
    Autenticación mediante token almacenado en una cookie HttpOnly.
    """

    def authenticate(self, request):
        cookie_name = "auth_token"
        token = request.COOKIES.get(cookie_name)

        if not token:
            return None

        self.enforce_csrf(request)

        return self.authenticate_credentials(token)

    def enforce_csrf(self, request):
        check = CsrfViewMiddleware(lambda req: None)
        resultado = check.process_view(request, None, (), {})

        if resultado:
            raise AuthenticationFailed(
                "La verificación CSRF falló."
            )
