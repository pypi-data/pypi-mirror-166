""" User Income Set Command Definition """
import requests

from rowantree.common.sdk import demand_env_var

from ...contracts.requests.user.income_set import UserIncomeSetRequest
from ..abstract_command import AbstractCommand


class UserIncomeSetCommand(AbstractCommand):
    """
    User Income Set Command
    Sets a user income. (Creates or dismisses a number of workers of the type).

    Methods
    -------
    execute(self, user_guid: str, request: UserIncomeSetRequest) -> None
        Executes the command.
    """

    def execute(self, user_guid: str, request: UserIncomeSetRequest, headers: dict[str, str]) -> None:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        request: UserIncomeSetRequest
            The UserIncomeSetRequest object for the update.
        headers: dict[str, str]
            Request headers
        """

        requests.post(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/income",
            data=request.json(by_alias=True),
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
