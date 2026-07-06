from __future__ import annotations

from typing import Any

import requests

from api.clients.base_api_client import BaseAPIClient


class BookingAPI:
    def __init__(self, client: BaseAPIClient) -> None:
        self.client = client

    def get_booking_ids(self, params: dict[str, Any] | None = None) -> requests.Response:
        return self.client.get("/booking", params=params)

    def get_booking(self, booking_id: int | str) -> requests.Response:
        return self.client.get(f"/booking/{booking_id}")

    def create_booking(self, payload: dict[str, Any]) -> requests.Response:
        return self.client.post("/booking", json=payload)

    def update_booking(
        self,
        booking_id: int | str,
        payload: dict[str, Any],
        token: str | None = None,
    ) -> requests.Response:
        return self.client.put(
            f"/booking/{booking_id}",
            json=payload,
            headers=self._auth_headers(token),
        )

    def partial_update_booking(
        self,
        booking_id: int | str,
        payload: dict[str, Any],
        token: str | None = None,
    ) -> requests.Response:
        return self.client.patch(
            f"/booking/{booking_id}",
            json=payload,
            headers=self._auth_headers(token),
        )

    def delete_booking(self, booking_id: int | str, token: str | None = None) -> requests.Response:
        return self.client.delete(
            f"/booking/{booking_id}",
            headers=self._auth_headers(token),
        )

    @staticmethod
    def _auth_headers(token: str | None) -> dict[str, str]:
        if not token:
            return {}
        return {"Cookie": f"token={token}"}
