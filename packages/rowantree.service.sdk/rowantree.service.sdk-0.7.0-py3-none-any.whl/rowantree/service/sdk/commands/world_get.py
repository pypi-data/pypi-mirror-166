""" World Status Get Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import WorldStatus

from .abstract_command import AbstractCommand


class WorldStatusGetCommand(AbstractCommand):
    """
    World Status Get Command
    Gets the world status.

    Methods
    -------
    execute(self) -> WorldStatus
        Executes the command.
    """

    def execute(self, headers: dict[str, str]) -> WorldStatus:
        """
        Executes the command.

        Returns
        -------
        world_status: WorldStatus
            The world status.
        headers: dict[str, str]
            Request headers
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/world",
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return WorldStatus.parse_obj(response.json())
