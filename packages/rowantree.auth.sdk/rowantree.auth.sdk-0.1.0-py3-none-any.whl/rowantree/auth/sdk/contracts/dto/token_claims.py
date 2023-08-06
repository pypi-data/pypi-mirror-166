from datetime import datetime

from pydantic import BaseModel


class TokenClaims(BaseModel):
    sub: str
    iss: str
    exp: datetime
    disabled: bool
    admin: bool
