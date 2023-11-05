from iocontrol.errors import AppException


class UnsupportedStructure(AppException):
    """The structure is not supported by the provisioner."""
