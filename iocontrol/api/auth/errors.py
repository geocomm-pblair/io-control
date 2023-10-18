from iocontrol.errors import AppException


class ForbiddenException(AppException):
    """Forbidden."""

    status_code: int = 403
