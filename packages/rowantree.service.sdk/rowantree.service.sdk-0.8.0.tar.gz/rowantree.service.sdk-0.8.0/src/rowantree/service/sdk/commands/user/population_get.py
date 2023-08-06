""" User Population Get Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float
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

    def execute(self, user_guid: str, headers: dict[str, str]) -> UserPopulation:
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
        user_population: UserPopulation
            User population object.
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/population",
            headers=headers,
            timeout=demand_env_var_as_float(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserPopulation.parse_obj(response.json())
