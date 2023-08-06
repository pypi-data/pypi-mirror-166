""" User Income Get Command Definition """

import requests
from requests import Response

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

    def execute(self, user_guid: str) -> UserIncomes:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_incomes: UserIncomes
            A (unique) list of user incomes.
        """

        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/income", headers=self.headers, timeout=self.config.timeout
        )
        return UserIncomes.parse_obj(response.json())
