""" World Status Get Command Definition """

import requests
from requests import Response

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

    def execute(self) -> WorldStatus:
        """
        Executes the command.

        Returns
        -------
        world_status: WorldStatus
            The world status.
        """

        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/world", headers=self.headers, timeout=self.config.timeout
        )
        return WorldStatus.parse_obj(response.json())
