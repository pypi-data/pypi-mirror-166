from pydantic import BaseModel


class AuthenticateUserRequest(BaseModel):
    username: str
    password: str
