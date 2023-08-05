import requests
from requests import Response
from rowantree.contracts import UserStores

from ..abstract_command import AbstractCommand


class UserStoresGetCommand(AbstractCommand):
    def execute(self, user_guid: str) -> UserStores:
        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/stores", headers=self.headers, timeout=self.config.timeout
        )
        return UserStores.parse_obj(response.json())
