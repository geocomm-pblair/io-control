from ipaddress import ip_network

from sqlalchemy import TypeDecorator
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB


class IPv4Network(TypeDecorator):
    """
    Custom type decorator for PostgreSQL ``INET`` type.

    .. seealso::

        https://docs.sqlalchemy.org/en/13/core/custom_types.html#augmenting-existing-types
    """

    impl = postgresql.INET

    def process_bind_param(self, value, dialect):  # noqa
        if value is not None:
            return str(value)

    def process_result_value(self, value, dialect):  # noqa
        return ip_network(value)


__all__ = [IPv4Network, JSONB]
