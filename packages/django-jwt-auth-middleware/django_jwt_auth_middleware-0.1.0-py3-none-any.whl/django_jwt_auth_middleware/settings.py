from django.conf import settings
from appconf import AppConf

from logging import getLogger

logger = getLogger(__name__)


class DjangoJwtAuthMiddlewareSettings(AppConf):
    JWT_ACCESS_DURATION = 5  # minutes
    JWT_ACCESS_HEADER = "Authorization"
    JWT_ALGORITHM = "HS256"
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = "Strict"
    JWT_COOKIE_SECURE = True
    JWT_LOGOUT_ACCESS = True
    JWT_REFRESH_DURATION = 14  # days
    JWT_REFRESH_PATH = "/jwt/refresh/"

    def configure_jwt_access_duration(self, value):
        return (
            value
            if not hasattr(settings, "JWT_ACCESS_DURATION")
            else settings.JWT_ACCESS_DURATION
        )

    def configure_jwt_access_header(self, value):
        return (
            value
            if not hasattr(settings, "JWT_ACCESS_HEADER")
            else settings.JWT_ACCESS_HEADER
        )

    def configure_jwt_algorithm(self, value):
        return (
            value
            if not hasattr(settings, "JWT_ALGORITHM")
            else settings.JWT_ALGORITHM
        )

    def configure_jwt_cookie_httponly(self, value):
        return (
            value
            if not hasattr(settings, "JWT_COOKIE_HTTPONLY")
            else settings.JWT_COOKIE_HTTPONLY
        )

    def configure_jwt_cookie_samesite(self, value):
        return (
            value
            if not hasattr(settings, "JWT_COOKIE_SAMESITE")
            else settings.JWT_COOKIE_SAMESITE
        )

    def configure_jwt_cookie_secure(self, value):
        return (
            value
            if not hasattr(settings, "JWT_COOKIE_SECURE")
            else settings.JWT_COOKIE_SECURE
        )

    def configure_jwt_logout_access(self, value):
        return (
            value
            if not hasattr(settings, "JWT_LOGOUT_ACCESS")
            else settings.JWT_LOGOUT_ACCESS
        )

    def configure_jwt_refresh_duration(self, value):
        return (
            value
            if not hasattr(settings, "JWT_REFRESH_DURATION")
            else settings.JWT_REFRESH_DURATION
        )

    def configure_jwt_refresh_path(self, value):
        return (
            value
            if not hasattr(settings, "JWT_REFRESH_PATH")
            else settings.JWT_REFRESH_PATH
        )

    def configure(self):
        logger.debug(
            f"django_jwt_auth_middleware.settings: {self.configured_data}"
        )
        return self.configured_data
