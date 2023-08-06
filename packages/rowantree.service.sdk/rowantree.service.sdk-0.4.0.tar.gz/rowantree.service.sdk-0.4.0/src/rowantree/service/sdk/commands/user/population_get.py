""" User Population Get Command Definition """

import requests
from requests import Response

from rowantree.contracts import UserPopulation

from ..abstract_command import AbstractCommand


class UserPopulationGetCommand(AbstractCommand):
    """
    User Population Get Command
    Gets the user population.

    Methods
    -------
    execute(self, user_guid: str) -> UserPopulation
        Executes the command.
    """

    def execute(self, user_guid: str) -> UserPopulation:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_population: UserPopulation
            User population object.
        """

        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/population",
            headers=self.headers,
            timeout=self.config.timeout,
        )
        return UserPopulation.parse_obj(response.json())
