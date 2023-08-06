""" Action Queue Process Command Definition """

import requests

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import ActionQueue

from .abstract_command import AbstractCommand


class ActionQueueProcessCommand(AbstractCommand):
    """
    Action Queue Process Command
    Processes an action queue.

    Methods
    -------
    execute(self, request: ActionQueue) -> None
        Executes the command.
    """

    def execute(self, request: ActionQueue, headers: dict[str, str]) -> None:
        """
        Executes the command.

        Parameters
        ----------
        request: ActionQueue
            The action queue to process.
        headers: dict[str, str]
            Request headers
        """

        requests.post(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/world/queue",
            data=request.json(by_alias=True),
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
