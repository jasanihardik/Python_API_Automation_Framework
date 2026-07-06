from __future__ import annotations

import requests

from api.clients.base_api_client import BaseAPIClient


class HealthCheckAPI:
    def __init__(self, client: BaseAPIClient) -> None:
        self.client = client

    def ping(self) -> requests.Response:
        return self.client.get("/ping")
