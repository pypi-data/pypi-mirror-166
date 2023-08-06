""" User State Get Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import UserState

from ..abstract_command import AbstractCommand


class UserStateGetCommand(AbstractCommand):
    """
    User State Get Command
    Gets the user game state.

    Methods
    -------
    execute(self, user_guid: str) -> UserState
        Executes the command.
    """

    def execute(self, user_guid: str, headers: dict[str, str]) -> UserState:
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
        user_state: UserState
            The user state object.
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/state",
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserState.parse_obj(response.json())
