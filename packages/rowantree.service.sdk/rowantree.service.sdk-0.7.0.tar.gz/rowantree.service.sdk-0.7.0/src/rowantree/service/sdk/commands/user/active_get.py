""" UserActiveGet Command Definition """
import requests
from requests import Response

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import UserActive

from ..abstract_command import AbstractCommand


class UserActiveGetCommand(AbstractCommand):
    """
    User Active Get Command
    Gets the user active state.

    Methods
    -------
    execute(self, user_guid: str) -> UserActive
        Executes the command.
    """

    def execute(self, user_guid: str, headers: dict[str, str]) -> UserActive:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The user guid to look up.
        headers: dict[str, str]
            Request headers

        Returns
        -------
        user_active: UserActive
            The user active state object.
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/active",
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserActive.parse_obj(response.json())
