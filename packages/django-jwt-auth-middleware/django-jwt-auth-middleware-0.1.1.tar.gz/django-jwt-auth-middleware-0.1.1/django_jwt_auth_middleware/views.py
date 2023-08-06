from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse

from logging import getLogger
from json import loads as json_load

from .auth import JWTifier
from .settings import DjangoJwtAuthMiddlewareSettings

logger = getLogger(__name__)
local_settings = DjangoJwtAuthMiddlewareSettings()


def set_cookie(response, key, value, path="/"):
    response.set_cookie(
        key=key,
        value=value,
        path=path,
        samesite=local_settings.JWT_COOKIE_SAMESITE,
        httponly=local_settings.JWT_COOKIE_HTTPONLY,
        secure=local_settings.JWT_COOKIE_SECURE,
    )


class Login(View):
    def post(self, request):
        if (
            request.content_type == "application/json"
            and not request.user.is_authenticated
        ):
            json = json_load(request.body)
            username = json["username"]
            password = json["password"]
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

        user = (
            authenticate(username=username, password=password) or request.user
        )

        if user.is_authenticated:
            jwtifier = JWTifier(user)
            access, refresh = jwtifier.create_refresh()

            response = JsonResponse(
                {"message": "Authentication successful."}, status=200
            )

            set_cookie(
                response, local_settings.JWT_ACCESS_HEADER, f"Bearer {access}"
            )
            set_cookie(
                response,
                f"Refresh{local_settings.JWT_ACCESS_HEADER}",
                f"{refresh}",
                path=local_settings.JWT_REFRESH_PATH,
            )

            return response

        else:
            return JsonResponse(
                {"message": "Valid user credentials not provided."}, status=400
            )


class Logout(View):
    def post(self, request):
        if request.user.is_authenticated:
            response = JsonResponse({"message": "Session ended."}, status=200)
            if local_settings.JWT_LOGOUT_ACCESS:
                set_cookie(response, local_settings.JWT_ACCESS_HEADER, "")
            set_cookie(
                response,
                f"Refresh{local_settings.JWT_ACCESS_HEADER}",
                "",
                path=local_settings.JWT_REFRESH_PATH,
            )
            return response
        else:
            return JsonResponse(
                {"message": "Must be authenticated to log out."}, status=401
            )


class Refresh(View):
    def post(self, request):
        try:
            # check for a valid refresh token
            token_str = request.META.get(
                f"HTTP_REFRESH{local_settings.JWT_ACCESS_HEADER}".upper()
            ) or request.COOKIES.get(
                f"Refresh{local_settings.JWT_ACCESS_HEADER}"
            )

            token = JWTifier.token_from_str(token_str)
            logger.debug(token)
            assert token is not None
            assert token["user"].is_active

            jwtifier = JWTifier(token["user"])
            assert jwtifier.validate_token(token_str, "refresh")
            access = jwtifier.create_access()

            response = JsonResponse(
                {"message": "Access token refreshed."}, status=200
            )
            set_cookie(
                response, local_settings.JWT_ACCESS_HEADER, f"Bearer {access}"
            )
            return response
        except (AssertionError, ValueError):
            return JsonResponse(
                {"message": "Invalid refresh token."}, status=403
            )
