""" User Feature Active Get Command """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float
from rowantree.contracts import UserFeature

from ..abstract_command import AbstractCommand


class UserFeatureActiveGetCommand(AbstractCommand):
    """
    User Feature Active Get Command
    Gets the active user feature.

    Methods
    -------
    execute(self, user_guid: str, details: bool) -> UserFeature
        Executes the command.
    """

    def execute(self, user_guid: str, details: bool, headers: dict[str, str]) -> UserFeature:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        details: bool
            Whether to include details of the feature.
        headers: dict[str, str]
            Request headers

        Returns
        -------
        user_feature: UserFeature
            The active UserFeature.
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/features/active",
            params={"details": details},
            headers=headers,
            timeout=demand_env_var_as_float(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserFeature.parse_obj(response.json())
