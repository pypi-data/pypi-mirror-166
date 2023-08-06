""" Action Queue Process Command Definition """

import json
import logging

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float

from ..contracts.dto.authenticate_user_request import AuthenticateUserRequest
from ..contracts.dto.token import Token
from .abstract_command import AbstractCommand


class AuthenticateUserCommand(AbstractCommand):
    """
    Authenticate User Command

    Methods
    -------
    execute(self, request: AuthenticateUserRequest) -> None
        Executes the command.
    """

    def execute(self, request: AuthenticateUserRequest) -> Token:
        """
        Executes the command.

        Parameters
        ----------
        request: AuthenticateUserRequest
        """

        request_dict: dict = {
            "url": f"{demand_env_var(name='ACCESS_AUTH_ENDPOINT')}/v1/auth/token",
            "data": request.dict(by_alias=True),
            "headers": self.headers,
            "timeout": demand_env_var_as_float(name="ACCESS_AUTH_ENDPOINT_TIMEOUT"),
        }
        logging.debug(json.dumps(request_dict))
        response: Response = requests.post(**request_dict)

        return Token.parse_obj(response.json())
