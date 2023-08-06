""" User Merchant Transforms Get Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float
from rowantree.contracts import UserMerchants

from ..abstract_command import AbstractCommand


class UserMerchantTransformsGetCommand(AbstractCommand):
    """
    User Merchant Transforms Get Command
    Gets a (unique) list of user merchant transforms.

    Methods
    -------
    execute(self, user_guid: str) -> UserMerchants
        Executes the command.
    """

    def execute(self, user_guid: str, headers: dict[str, str]) -> UserMerchants:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            Target user guid.
        headers: dict[str, str]
            Request headers

        Returns
        -------
        user_merchants: UserMerchants
            A (unique) list of user merchant transforms.
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/merchant",
            headers=headers,
            timeout=demand_env_var_as_float(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return UserMerchants.parse_obj(response.json())
