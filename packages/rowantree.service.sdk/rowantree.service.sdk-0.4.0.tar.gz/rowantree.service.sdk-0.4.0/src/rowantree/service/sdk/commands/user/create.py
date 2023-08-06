""" User Create Command Definition """

import requests
from requests import Response

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

    def execute(self) -> User:
        """
        Executes the command.

        Returns
        -------
        user: User
            The newly created user.
        """

        response: Response = requests.post(
            url=f"{self.config.endpoint}/v1/user", headers=self.headers, timeout=self.config.timeout
        )
        return User.parse_obj(response.json())
