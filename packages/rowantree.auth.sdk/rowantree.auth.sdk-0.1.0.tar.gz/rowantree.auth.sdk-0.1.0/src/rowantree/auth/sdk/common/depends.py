from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException

from ..config.auth import AuthConfig
from ..contracts.dto.token_claims import TokenClaims
from .claims import get_claims

# Generating auth configuration
auth_config: AuthConfig = AuthConfig()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{auth_config.auth_endpoint}/v1/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenClaims:
    return get_claims(token=token)


async def is_enabled(token_claims: TokenClaims = Depends(get_current_user)) -> TokenClaims:
    if token_claims.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return token_claims


async def is_admin(token_claims: TokenClaims = Depends(is_enabled)) -> TokenClaims:
    if not token_claims.admin:
        raise HTTPException(status_code=400, detail="Insufficient Permissions")
    return token_claims
