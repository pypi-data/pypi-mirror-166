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
    access_key: Optional[str]
    endpoint: Optional[str]
    timeout: Optional[float]

    def __init__(self, **data: Any):
        super().__init__(**data)
        config = configparser.ConfigParser()
        config.read(self.config_file_path)

        # Server Options
        self.access_key = config.get("SERVER", "access_key")
        self.endpoint = config.get("SERVER", "endpoint")
        self.timeout = config.getfloat("SERVER", "timeout")

        if "ACCESS_KEY" in os.environ:
            self.access_key = os.environ["ACCESS_KEY"]

        if "ROWANTREE_SERVICE_ENDPOINT" in os.environ:
            self.endpoint = os.environ["ROWANTREE_SERVICE_ENDPOINT"]

        if "ROWANTREE_SERVICE_TIMEOUT" in os.environ:
            self.timeout = float(os.environ["ROWANTREE_SERVICE_TIMEOUT"])
