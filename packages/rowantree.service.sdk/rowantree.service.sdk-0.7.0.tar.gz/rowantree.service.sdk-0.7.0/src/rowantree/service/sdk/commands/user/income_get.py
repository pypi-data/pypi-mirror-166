""" User Income Get Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import UserIncomes

from ..abstract_command import AbstractCommand


class UserIncomeGetCommand(AbstractCommand):
    """
    User Income Get Command
    Gets (unique) list of user incomes.

    Methods
    -------
    execute(self, user_guid: str) -> UserIncomes
        Executes the command.
    """

    def execute(self, user_guid: str, headers: dict[str, str]) -> UserIncomes:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        headers: dict[str, str]
            Request headers

        Returns
        -------
        user_incomes: UserIncomes
            A (unique) list of user incomes.
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/income",
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserIncomes.parse_obj(response.json())
