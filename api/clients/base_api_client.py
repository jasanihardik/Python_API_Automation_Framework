from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import requests

from utils.logger import get_logger


class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.default_headers = default_headers or {}
        self.session = requests.Session()
        self.logger = get_logger(self.__class__.__name__)

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        return self._send("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        return self._send("POST", path, json=json, data=data, headers=headers)

    def put(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        return self._send("PUT", path, json=json, headers=headers)

    def patch(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        return self._send("PATCH", path, json=json, headers=headers)

    def delete(
        self,
        path: str,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        return self._send("DELETE", path, headers=headers)

    def _send(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        url = self._build_url(path)
        merged_headers = self._merge_headers(headers)

        self.logger.info("Request: %s %s", method, url)
        if params:
            self.logger.info("Request params: %s", params)
        if json:
            self.logger.info("Request json: %s", json)

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=merged_headers,
            timeout=self.timeout,
        )

        elapsed_ms = response.elapsed.total_seconds() * 1000
        self.logger.info(
            "Response: %s %s | Status: %s | Time: %.2f ms",
            method,
            url,
            response.status_code,
            elapsed_ms,
        )

        if response.status_code >= 400:
            self.logger.info("Error response body: %s", response.text)

        return response

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return urljoin(self.base_url, path.lstrip("/"))

    def _merge_headers(self, headers: dict[str, str] | None) -> dict[str, str]:
        merged_headers = self.default_headers.copy()
        if headers:
            merged_headers.update(headers)
        return merged_headers
