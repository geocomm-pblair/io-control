"""
NOTE TO THE FUTURE: This is a "vendor-ized" copy of Frontegg's
`frontegg.fastapi.secure_access.frontegg_security` module.  The `User` class
in the original module specifies some fields as "Optional" but doesn't
provide defaults.  With pydantic 2.4.0 this seems to cause a validation error
if the "superUser" and "createdByUserId" values are missing from the token.

If you're reading this, please check **right now** to see if this has been
corrected in the latest version.
"""
import enum
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

import frontegg
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.security.base import SecurityBase
from fastapi.security.http import HTTPBearerModel
from frontegg.common.clients.types import AuthHeaderType
from frontegg.helpers.exceptions import UnauthorizedException
from frontegg.helpers.logger import logger
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class TokenType(str, enum.Enum):
    UserToken = "userToken"
    UserApiToken = "userApiToken"
    TenantApiToken = "tenantApiToken"
    TenantAccessToken = "tenantAccessToken"
    UserAccessToken = "userAccessToken"


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # Fields which are general for all kinds of tokens
    sub: str
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    tenant_id: str = Field(alias="tenantId")

    token_type: TokenType = Field(alias="type")
    access_token: str

    # User token fields - all fields must be optional to support API tokens
    metadata: Optional[Dict[str, Any]]
    name: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    tenant_ids: Optional[List[str]] = Field(
        alias="tenantIds", default_factory=list
    )
    profile_picture_url: Optional[str] = Field(alias="profilePictureUrl")
    super_user: Optional[bool] = Field(default=None, alias="superUser")

    # API Token fields - all fields must be optional to support user tokens
    created_by_user_id: Optional[str] = Field(
        default=None, alias="createdByUserId"
    )

    def has_permissions(self, permissions: List[str]) -> bool:
        return bool(permissions) and all(
            p in self.permissions for p in permissions
        )

    def has_roles(self, roles: List[str]) -> bool:
        return bool(roles) and all(r in self.roles for r in roles)

    @property
    def id(self) -> Optional[str]:
        """
        When using tenant API Token, there is no user ID.
        When using user API Token, the user ID is specified in the
        created_by_user_id field.
        Otherwise, the user ID is specified in the sub field.
        """
        if self.token_type == TokenType.TenantApiToken:
            return None

        return self.created_by_user_id or self.sub


class FronteggHTTPAuthentication(SecurityBase):
    def __init__(
        self,
        bearerFormat: Optional[str] = None,  # noqa
        scheme_name: Optional[str] = None,
        auto_error: bool = True,
        roles: List[str] = [],
        permissions: List[str] = [],
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.roles = roles
        self.permissions = permissions

    def handle_authentication_failure(self) -> None:
        if self.auto_error:
            raise HTTPException(status_code=401, detail="Unauthenticated")
        else:
            return None

    async def __call__(self, request: Request) -> Optional[User]:
        try:
            auth_header = get_auth_header(request)
            if auth_header is None:
                raise HTTPException(status_code=401, detail="Unauthenticated")

            decoded_user = (
                frontegg.fastapi.frontegg.validate_identity_on_token(
                    auth_header.get("token"),
                    {"roles": self.roles, "permissions": self.permissions},
                    auth_header.get("type"),
                )
            )
            return User(**decoded_user, access_token=auth_header.get("token"))

        except UnauthorizedException:
            logger.info("entity does not have required role and permissions")
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action.",
            )

        except Exception as e:
            logger.error(
                "something went wrong while validating JWT, " + str(e)
            )
            return self.handle_authentication_failure()


def FronteggSecurity(
    permissions: List[str] = [], auto_error: bool = True, roles: List[str] = []
) -> Callable[[], User]:
    """
    This factory function will create an authentication dependency for FastAPI,
    and will ensure the user has the right permissions if specified.
    """

    def check_perm(
        user: User = Depends(
            FronteggHTTPAuthentication(
                auto_error=auto_error, roles=roles, permissions=permissions
            )
        )
    ) -> User:
        return user

    return check_perm


def get_auth_header(req: Request) -> Optional[Dict[str, Any]]:
    token = req.headers.get("Authorization")
    if token is not None:
        return {
            "token": token.replace("Bearer ", ""),
            "type": AuthHeaderType.JWT.value,
        }

    token = req.headers.get("x-api-key")
    if token is not None:
        return {"token": token, "type": AuthHeaderType.AccessToken.value}

    return None
