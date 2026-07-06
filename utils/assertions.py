from __future__ import annotations

from typing import Any

import requests


def assert_status_code(response: requests.Response, expected_status_code: int) -> None:
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, got {actual_status_code}. "
        f"Response body: {response.text}"
    )


def assert_response_time_under(response: requests.Response, max_ms: int) -> None:
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms <= max_ms, (
        f"Expected response time under {max_ms} ms, got {elapsed_ms:.2f} ms "
        f"for {response.request.method} {response.url}"
    )


def assert_json_key_exists(response_json: dict[str, Any], key: str) -> None:
    assert key in response_json, f"Expected key '{key}' in response: {response_json}"


def assert_json_value(response_json: dict[str, Any], key: str, expected_value: Any) -> None:
    assert_json_key_exists(response_json, key)
    actual_value = response_json[key]
    assert actual_value == expected_value, (
        f"Expected '{key}' to be '{expected_value}', got '{actual_value}'. "
        f"Response: {response_json}"
    )
