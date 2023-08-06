""" Merchant Transforms Perform Command Definition """

import requests

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

    def execute(self, user_guid: str, request: MerchantTransformRequest) -> None:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        request: MerchantTransformRequest
            The merchant transform request.
        """

        requests.post(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/merchant",
            data=request.json(by_alias=True),
            headers=self.headers,
            timeout=self.config.timeout,
        )
