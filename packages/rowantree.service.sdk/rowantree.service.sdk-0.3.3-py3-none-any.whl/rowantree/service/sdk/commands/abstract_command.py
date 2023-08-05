from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..common.config import Config


class AbstractCommand(BaseModel):
    config: Config
    headers: dict[str, str] = {}
    timeout: float = 30

    def __init__(self, **data: Any):
        super().__init__(**data)
        if "API-ACCESS-KEY" not in self.headers:
            self.headers["API-ACCESS-KEY"] = self.config.access_key

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Command entry point"""
