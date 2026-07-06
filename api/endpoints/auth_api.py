from __future__ import annotations

import requests

from api.clients.base_api_client import BaseAPIClient


class AuthAPI:
    def __init__(self, client: BaseAPIClient) -> None:
        self.client = client

    def create_token(self, username: str, password: str) -> requests.Response:
        payload = {
            "username": username,
            "password": password,
        }
        return self.client.post("/auth", json=payload)
