""" Auth Service Register User Base Definition """

from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    """
    Auth Service Register User Base

    Attributes
    ----------
    username: str
        The username of the user.
    email: Union[str, None] = None
        The user email address.
    hashed_password: str
        Hashed user password.
    """

    username: str
    email: str
    hashed_password: str
