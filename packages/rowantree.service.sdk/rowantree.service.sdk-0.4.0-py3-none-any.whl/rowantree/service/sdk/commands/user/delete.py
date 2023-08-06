""" User Delete Command Definition """

import requests

from ..abstract_command import AbstractCommand


class UserDeleteCommand(AbstractCommand):
    """
    User Delete Command
    Deletes a user.

    Methods
    -------
    execute(self, user_guid: str) -> None
        Executes the command.
    """

    def execute(self, user_guid: str) -> None:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        """

        requests.delete(
            url=f"{self.config.endpoint}/v1/user/{user_guid}", headers=self.headers, timeout=self.config.timeout
        )
