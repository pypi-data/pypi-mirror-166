import requests
from requests import Response
from rowantree.contracts import UserFeatures

from ..abstract_command import AbstractCommand


class UserFeaturesGetCommand(AbstractCommand):
    def execute(self, user_guid: str) -> UserFeatures:
        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/features",
            headers=self.headers,
            timeout=self.config.timeout,
        )
        return UserFeatures.parse_obj(response.json())
