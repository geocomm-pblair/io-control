from iocontrol.errors import AppException


class UnauthorizedException(AppException):
    """Unauthorized."""

    status_code: int = 401


class ForbiddenException(AppException):
    """Forbidden."""

    status_code: int = 403
