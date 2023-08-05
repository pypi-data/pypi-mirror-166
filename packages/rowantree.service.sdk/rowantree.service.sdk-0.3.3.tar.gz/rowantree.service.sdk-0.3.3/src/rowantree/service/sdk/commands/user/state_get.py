import requests
from requests import Response
from rowantree.contracts import UserState

from ..abstract_command import AbstractCommand


class UserStateGetCommand(AbstractCommand):
    def execute(self, user_guid: str) -> UserState:
        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/state", headers=self.headers, timeout=self.config.timeout
        )
        return UserState.parse_obj(response.json())
