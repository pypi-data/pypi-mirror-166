import requests
from requests import Response
from rowantree.contracts import UserFeature

from ..abstract_command import AbstractCommand


class UserFeatureActiveGetCommand(AbstractCommand):
    def execute(self, user_guid: str, details: bool) -> UserFeature:
        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/features/active",
            params={"details": details},
            headers=self.headers,
            timeout=self.config.timeout,
        )
        return UserFeature.parse_obj(response.json())
