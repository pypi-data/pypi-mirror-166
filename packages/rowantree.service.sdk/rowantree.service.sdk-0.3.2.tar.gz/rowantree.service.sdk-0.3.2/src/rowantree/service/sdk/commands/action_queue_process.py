import requests

from ..contracts.requests.action_queue_process import ActionQueueProcessRequest
from .abstract_command import AbstractCommand


class ActionQueueProcessCommand(AbstractCommand):
    def execute(self, request: ActionQueueProcessRequest) -> None:
        requests.post(
            url=f"{self.config.endpoint}/v1/world/queue",
            data=request.json(by_alias=True),
            headers=self.headers,
            timeout=self.config.timeout,
        )
