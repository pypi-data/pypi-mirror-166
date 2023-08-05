import requests
from requests import Response
from rowantree.contracts import WorldStatus

from .abstract_command import AbstractCommand


class WorldStatusGetCommand(AbstractCommand):
    def execute(self) -> WorldStatus:
        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/world", headers=self.headers, timeout=self.config.timeout
        )
        return WorldStatus.parse_obj(response.json())
