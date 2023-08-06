""" User Create Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import User

from ..abstract_command import AbstractCommand


class UserCreateCommand(AbstractCommand):
    """
    User Create Command
    Creates a user.

    Methods
    -------
    execute(self) -> User
        Executes the command.
    """

    def execute(self, headers: dict[str, str]) -> User:
        """
        Executes the command.

        Parameters
        ----------
        headers: dict[str, str]
            Request headers

        Returns
        -------
        user: User
            The newly created user.
        """

        response: Response = requests.post(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user",
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return User.parse_obj(response.json())
