""" Action Queue Process Command Definition """
import json
import logging

import requests
from requests import Response

from .abstract_command import AbstractCommand
from ..contracts.dto.authenticate_user_request import AuthenticateUserRequest
from ..contracts.dto.token import Token


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
            "url": f"{self.config.auth_endpoint}/v1/auth/token",
            "data": request.dict(by_alias=True),
            "headers": self.headers,
            "timeout": self.config.timeout,
        }
        logging.debug(json.dumps(request_dict))
        response: Response = requests.post(**request_dict)

        return Token.parse_obj(response.json())
