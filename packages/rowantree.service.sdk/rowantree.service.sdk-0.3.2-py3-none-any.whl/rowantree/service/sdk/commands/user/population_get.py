import requests
from requests import Response
from rowantree.contracts import UserPopulation

from ..abstract_command import AbstractCommand


class UserPopulationGetCommand(AbstractCommand):
    def execute(self, user_guid: str) -> UserPopulation:
        response: Response = requests.post(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/population",
            headers=self.headers,
            timeout=self.config.timeout,
        )
        return UserPopulation.parse_obj(response.json())
