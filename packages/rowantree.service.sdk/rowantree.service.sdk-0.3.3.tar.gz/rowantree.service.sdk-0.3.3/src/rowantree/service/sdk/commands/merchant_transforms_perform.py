import requests

from ..contracts.requests.merchant_transform import MerchantTransformRequest
from .abstract_command import AbstractCommand


class MerchantTransformPerformCommand(AbstractCommand):
    def execute(self, user_guid: str, request: MerchantTransformRequest) -> None:
        requests.post(
            url=f"{self.config.endpoint}/v1/user/{user_guid}/merchant",
            data=request.json(by_alias=True),
            headers=self.headers,
            timeout=self.config.timeout,
        )
