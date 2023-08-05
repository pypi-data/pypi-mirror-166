from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model, authenticate
from django.utils.deprecation import MiddlewareMixin
from jwt.exceptions import DecodeError, ExpiredSignatureError
from django.utils import timezone
from django.conf import settings as django_settings
from jwt import decode as jwt_decode, encode as jwt_encode

from datetime import timedelta
from logging import getLogger
from secrets import token_hex

from .settings import DjangoJwtAuthMiddlewareSettings

logger = getLogger(__name__)
local_settings = DjangoJwtAuthMiddlewareSettings()


class JWTifier:
    def __init__(self, user):
        self.user = user

    @classmethod
    def __encode(cls, user, duration, tok_type):
        now = timezone.now()
        jwt = jwt_encode(
            {
                "iat": now,
                "exp": now + duration,
                # "exp": now,
                "user": str(user.id),
                "tok": tok_type,
                "sec": token_hex(16),
            },
            django_settings.SECRET_KEY,
            algorithm=local_settings.JWT_ALGORITHM,
        )
        return jwt

    def create_access(
        self, duration=timedelta(minutes=local_settings.JWT_ACCESS_DURATION)
    ):
        return self.__encode(self.user, duration, "access")

    def create_refresh(
        self, duration=timedelta(days=local_settings.JWT_REFRESH_DURATION)
    ):
        return self.create_access(), self.__encode(
            self.user, duration, "refresh"
        )

    @classmethod
    def __decode(cls, jwt):
        try:
            token = jwt_decode(
                jwt,
                django_settings.SECRET_KEY,
                algorithms=local_settings.JWT_ALGORITHM,
            )
            user = get_user_model().objects.get(
                pk=token["user"], is_active=True
            )
            token["user"] = user
            return token
        except (
            DecodeError,
            ExpiredSignatureError,
            get_user_model().DoesNotExist,
        ):
            return None

    def validate_token(self, jwt, tok_type):
        token = self.__decode(jwt) or {"user": None, "tok": None}
        return token["user"] == self.user and token["tok"] == tok_type

    @classmethod
    def user_from_token(cls, jwt):
        token = cls.__decode(jwt) or {"user": None}
        return token["user"]

    @classmethod
    def token_from_str(cls, jwt):
        return cls.__decode(jwt)


class JWTAuthenticationBackend(BaseBackend):
    def authenticate(self, request, token=None):
        try:
            auth_type, auth_str = token.split(" ")
            assert auth_type.lower() == "bearer"

            return JWTifier.user_from_token(auth_str)
        except (
            AssertionError,
            get_user_model().DoesNotExist,
            ExpiredSignatureError,
            DecodeError,
            ValueError,
        ):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id, is_active=True)
        except get_user_model().DoesNotExist:
            return None


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated and (
            f"HTTP_{local_settings.JWT_ACCESS_HEADER.upper()}" in request.META
            or local_settings.JWT_ACCESS_HEADER in request.COOKIES
        ):
            auth_token_str = request.META.get(
                f"HTTP_{local_settings.JWT_ACCESS_HEADER.upper()}"
            ) or request.COOKIES.get(local_settings.JWT_ACCESS_HEADER)
            request.user = (
                authenticate(request, token=auth_token_str) or AnonymousUser()
            )
