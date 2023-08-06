""" Abstract Command Definition """

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from rowantree.auth.sdk.commands.authenticate_user import AuthenticateUserCommand
from rowantree.auth.sdk.config.auth import AuthConfig
from rowantree.auth.sdk.contracts.dto.authenticate_user_request import AuthenticateUserRequest
from rowantree.auth.sdk.contracts.dto.token import Token

from ..common.config import Config


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

    config: Config
    headers: dict[str, str] = {}
    timeout: float = 30

    def __init__(self, **data: Any):
        super().__init__(**data)

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Command entry point"""
