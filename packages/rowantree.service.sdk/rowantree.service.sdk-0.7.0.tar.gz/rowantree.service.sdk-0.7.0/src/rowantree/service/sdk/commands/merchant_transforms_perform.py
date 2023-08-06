""" Merchant Transforms Perform Command Definition """

import requests

from rowantree.common.sdk import demand_env_var

from ..contracts.requests.merchant_transform import MerchantTransformRequest
from .abstract_command import AbstractCommand


class MerchantTransformPerformCommand(AbstractCommand):
    """
    Merchant Transform Perform Command
    Performs a merchant transform.

    Methods
    -------
    execute(self, user_guid: str, request: MerchantTransformRequest) -> None
        Executes the command.
    """

    def execute(self, user_guid: str, request: MerchantTransformRequest, headers: dict[str, str]) -> None:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        request: MerchantTransformRequest
            The merchant transform request.
        headers: dict[str, str]
            Request headers
        """

        requests.post(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/merchant",
            data=request.json(by_alias=True),
            headers=headers,
            timeout=demand_env_var(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
