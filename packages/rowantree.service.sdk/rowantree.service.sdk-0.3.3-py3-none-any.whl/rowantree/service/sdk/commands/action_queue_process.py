import requests
from rowantree.contracts import ActionQueue

from .abstract_command import AbstractCommand


class ActionQueueProcessCommand(AbstractCommand):
    def execute(self, request: ActionQueue) -> None:
        requests.post(
            url=f"{self.config.endpoint}/v1/world/queue",
            data=request.json(by_alias=True),
            headers=self.headers,
            timeout=self.config.timeout,
        )
