from abc import ABC, abstractmethod
from typing import Any, Optional

from ..common.config import Config


class AbstractCommand(ABC):
    config: Config
    headers: dict[str, str]
    timeout: float = 30

    def __init__(self, config: Config):
        self.config = config
        self.headers["API-ACCESS-KEY"] = self.config.access_key

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Command entry point"""
