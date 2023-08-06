""" UserActiveGet Command Definition """
import requests
from requests import Response

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

    def execute(self, user_guid: str) -> UserActive:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The user guid to look up.

        Returns
        -------
        user_active: UserActive
            The user active state object.
        """

        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/active", headers=self.headers, timeout=self.config.timeout
        )
        return UserActive.parse_obj(response.json())
