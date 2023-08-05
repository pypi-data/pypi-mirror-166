import requests
from requests import Response
from rowantree.contracts import UserMerchants

from ..abstract_command import AbstractCommand


class UserMerchantTransformsGetCommand(AbstractCommand):
    def execute(self, user_guid: str) -> UserMerchants:
        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/merchant",
            headers=self.headers,
            timeout=self.config.timeout,
        )
        return UserMerchants.parse_obj(response.json())
