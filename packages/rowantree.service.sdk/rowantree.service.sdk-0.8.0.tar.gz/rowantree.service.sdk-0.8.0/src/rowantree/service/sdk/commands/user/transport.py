""" User Transport Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float
from rowantree.contracts import UserFeature

from ...contracts.requests.user.transport import UserTransportRequest
from ..abstract_command import AbstractCommand


class UserTransportCommand(AbstractCommand):
    """
    User Transport Command
    Performs a user transport. (feature to feature change)

    Methods
    -------
    execute(self, user_guid: str, request: UserTransportRequest) -> UserFeature
        Executes the command.
    """

    def execute(self, user_guid: str, request: UserTransportRequest, headers: dict[str, str]) -> UserFeature:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        request: UserTransportRequest
            The UserTransportRequest to perform.
        headers: dict[str, str]
            Request headers

        Returns
        -------
        user_feature: UserFeature
            The user's new active feature.
        """

        response: Response = requests.post(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/transport",
            data=request.json(by_alias=True),
            headers=headers,
            timeout=demand_env_var_as_float(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserFeature.parse_obj(response.json())
