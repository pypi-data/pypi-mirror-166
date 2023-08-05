import requests

from ...contracts.requests.user.income_set import UserIncomeSetRequest
from ..abstract_command import AbstractCommand


class UserIncomeSetCommand(AbstractCommand):
    def execute(self, user_guid: str, request: UserIncomeSetRequest) -> None:
        requests.post(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/income",
            data=request.json(by_alias=True),
            headers=self.headers,
            timeout=self.config.timeout,
        )
