""" Service Config Definition """

import configparser
import os
from typing import Optional

from pydantic import BaseModel


class AuthConfig(BaseModel):
    """
    Service Configuration
    """

    secret_key: Optional[str]
    algorithm: Optional[str]
    issuer: Optional[str]
    auth_endpoint: Optional[str]
    timeout: Optional[float]

    def __init__(self, *args, config_file_path: str = "rowantree.config", **kwargs):
        super().__init__(**kwargs)
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Server Options
        self.secret_key = config.get("SERVER", "secret_key")
        self.algorithm = config.get("SERVER", "algorithm")
        self.issuer = config.get("SERVER", "issuer")
        self.auth_endpoint = config.get("SERVER", "auth_endpoint")
        self.timeout = config.getfloat("SERVER", "timeout")

        if "ACCESS_TOKEN_SECRET_KEY" in os.environ:
            self.secret_key = os.environ["SECRET_KEY"]

        if "ACCESS_TOKEN_ALGORITHM" in os.environ:
            self.algorithm = os.environ["ALGORITHM"]

        if "ACCESS_TOKEN_ISSUER" in os.environ:
            self.issuer = os.environ["ACCESS_TOKEN_ISSUER"]

        if "ACCESS_AUTH_ENDPOINT" in os.environ:
            self.auth_endpoint = os.environ["ACCESS_AUTH_ENDPOINT"]

        if "ROWANTREE_AUTH_TIMEOUT" in os.environ:
            self.timeout = float(os.environ["ROWANTREE_AUTH_TIMEOUT"])
