import requests
from requests import Response
from rowantree.contracts import UserFeature

from ...contracts.requests.user.transport import UserTransportRequest
from ..abstract_command import AbstractCommand


class UserTransportCommand(AbstractCommand):
    def execute(self, user_guid: str, request: UserTransportRequest) -> UserFeature:
        response: Response = requests.post(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/transport",
            data=request.json(by_alias=True),
            headers=self.headers,
            timeout=self.config.timeout,
        )
        return UserFeature.parse_obj(response.json())
