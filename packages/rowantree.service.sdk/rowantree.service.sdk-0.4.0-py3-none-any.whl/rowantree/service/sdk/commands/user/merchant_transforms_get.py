""" User Merchant Transforms Get Command Definition """

import requests
from requests import Response

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

    def execute(self, user_guid: str) -> UserMerchants:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            Target user guid.

        Returns
        -------
        user_merchants: UserMerchants
            A (unique) list of user merchant transforms.
        """

        response: Response = requests.get(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/merchant",
            headers=self.headers,
            timeout=self.config.timeout,
        )
        return UserMerchants.parse_obj(response.json())
