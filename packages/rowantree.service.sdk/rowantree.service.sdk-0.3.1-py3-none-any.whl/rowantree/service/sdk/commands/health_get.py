import requests
from requests import Response

from .abstract_command import AbstractCommand


class HealthGetCommand(AbstractCommand):
    def execute(self) -> bool:
        response: Response = requests.get(url=f"{self.config.endpoint}/health/plain", timeout=self.config.timeout)
        return bool(response.text)


# if __name__ == "__main__":
#     active: bool = HealthGetCommand(config=Config()).execute()
#     print(active)
