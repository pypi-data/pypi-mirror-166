""" User Delete Command Definition """

import requests

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float

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

    def execute(self, user_guid: str, headers: dict[str, str]) -> None:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        headers: dict[str, str]
            Request headers
        """

        requests.delete(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}",
            headers=headers,
            timeout=demand_env_var_as_float(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
