import requests

from ..abstract_command import AbstractCommand


class UserDeleteCommand(AbstractCommand):
    def execute(self, user_guid: str) -> None:
        requests.delete(
            url=f"{self.config.endpoint}/v1/user/{user_guid}", headers=self.headers, timeout=self.config.timeout
        )
