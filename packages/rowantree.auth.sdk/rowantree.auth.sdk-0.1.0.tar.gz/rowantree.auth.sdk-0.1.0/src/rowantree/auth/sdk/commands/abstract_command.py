""" Abstract Command Definition """

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..config.auth import AuthConfig


class AbstractCommand(BaseModel):
    """
    Abstract Command

    Attributes
    ----------
    config: Config
        The configuration for the command.
    headers: dict[str, str] = {}
        Headers needed for the requests.
    timeout: float = 30
        The default timeout of requests.
    """

    config: AuthConfig
    headers: dict[str, str] = {}
    timeout: float = 30

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Command entry point"""
