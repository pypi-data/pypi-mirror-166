""" SDK Config Definition """

import configparser
import os
from typing import Any, Optional

from pydantic import BaseModel


class Config(BaseModel):
    """
    SDK Config
    Defines the high level environmental configurations/settings for the SDK.

    Attributes
    ----------
    config_file_path: Optional[str] = "rowantree.config"
        The config file to load.
    access_key: Optional[str]
        The service layer access key
    endpoint: Optional[str]
        The service layer endpoint - http(s)://(host):(port)
    timeout: Optional[float]
        The timeout for requests to the service layer.
    """

    config_file_path: Optional[str] = "rowantree.config"
    username: Optional[str]
    password: Optional[str]
    auth_endpoint: Optional[str]
    endpoint: Optional[str]
    timeout: Optional[float]

    def __init__(self, **data: Any):
        super().__init__(**data)
        config = configparser.ConfigParser()
        config.read(self.config_file_path)

        # Server Options
        self.username = config.get("SERVER", "username")
        self.password = config.get("SERVER", "password")
        self.auth_endpoint = config.get("SERVER", "auth_endpoint")
        self.endpoint = config.get("SERVER", "endpoint")
        self.timeout = config.getfloat("SERVER", "timeout")

        if "ACCESS_USERNAME" in os.environ:
            self.username = os.environ["ACCESS_USERNAME"]

        if "ACCESS_PASSWORD" in os.environ:
            self.password = os.environ["ACCESS_PASSWORD"]

        if "ACCESS_AUTH_ENDPOINT" in os.environ:
            self.auth_endpoint = os.environ["ACCESS_AUTH_ENDPOINT"]

        if "ROWANTREE_SERVICE_ENDPOINT" in os.environ:
            self.endpoint = os.environ["ROWANTREE_SERVICE_ENDPOINT"]

        if "ROWANTREE_SERVICE_TIMEOUT" in os.environ:
            self.timeout = float(os.environ["ROWANTREE_SERVICE_TIMEOUT"])
