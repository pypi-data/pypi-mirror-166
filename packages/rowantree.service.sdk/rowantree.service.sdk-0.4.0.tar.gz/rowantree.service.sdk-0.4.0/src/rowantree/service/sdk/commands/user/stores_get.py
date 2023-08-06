""" User Stores Get Command Definition """

import requests
from requests import Response

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

    def execute(self, user_guid: str) -> UserStores:
        """
        Gets the (unique) list of user stores.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_stores: UserStores
            A (unique) list of user stores.
        """

        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/stores", headers=self.headers, timeout=self.config.timeout
        )
        return UserStores.parse_obj(response.json())
