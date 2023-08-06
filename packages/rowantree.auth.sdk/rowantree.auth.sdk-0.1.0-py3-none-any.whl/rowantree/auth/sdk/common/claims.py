import logging
from typing import Optional

from jose import JWTError, jwt
from starlette import status
from starlette.exceptions import HTTPException

from ..config.auth import AuthConfig
from ..contracts.dto.token_claims import TokenClaims

# Generating auth configuration
auth_config: AuthConfig = AuthConfig()


def get_claims(token: str) -> TokenClaims:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(
            token, auth_config.secret_key, algorithms=[auth_config.algorithm], issuer=auth_config.issuer
        )
        issuer: Optional[str] = payload.get("iss")
        guid: Optional[str] = payload.get("sub")
        if issuer != auth_config.issuer or guid is None:
            logging.debug(f"Received issuer: {issuer}, expected: {auth_config.issuer}, guid was: {guid}")
            raise credentials_exception
        logging.debug(payload)
        return TokenClaims(**payload)
    except JWTError:
        raise credentials_exception
