import requests
from requests import Response
from rowantree.contracts import User

from ..abstract_command import AbstractCommand


class UserCreateCommand(AbstractCommand):
    def execute(self) -> User:
        response: Response = requests.post(
            url=f"{self.config.endpoint}/v1/user", headers=self.headers, timeout=self.config.timeout
        )
        return User.parse_obj(response.json())
