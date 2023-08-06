""" User Stores Get Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import UserStores

from ..abstract_command import AbstractCommand


class UserStoresGetCommand(AbstractCommand):
    """
    User Stores Get Command
    Gets the (unique) list of user stores.

    Methods
    -------
    execute(self, user_guid: str) -> UserStores
        Executes the command.
    """

    def execute(self, user_guid: str, headers: dict[str, str]) -> UserStores:
        """
        Gets the (unique) list of user stores.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        headers: dict[str, str]
            Request headers

        Returns
        -------
        user_stores: UserStores
            A (unique) list of user stores.
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/stores",
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserStores.parse_obj(response.json())
