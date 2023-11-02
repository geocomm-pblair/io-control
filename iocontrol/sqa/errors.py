from iocontrol.errors import AppException


class DataInconsistencyException(AppException):
    """We detected an inconsistency in the data."""

    status_code: int = 500
