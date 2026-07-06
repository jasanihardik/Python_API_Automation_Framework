from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from api.clients.base_api_client import BaseAPIClient
from api.endpoints.auth_api import AuthAPI
from api.endpoints.booking_api import BookingAPI
from api.endpoints.health_check_api import HealthCheckAPI
from api.schemas.auth_schema import AUTH_TOKEN_SCHEMA
from config.config_loader import (
    get_auth_credentials,
    get_base_url,
    get_default_headers,
    get_max_response_time_ms,
    get_timeout,
)
from utils.assertions import assert_response_time_under, assert_status_code
from utils.data_generator import generate_booking_payload
from utils.schema_validator import validate_json_schema

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def api_client() -> BaseAPIClient:
    return BaseAPIClient(
        base_url=get_base_url(),
        timeout=get_timeout(),
        default_headers=get_default_headers(),
    )


@pytest.fixture(scope="session")
def auth_api(api_client: BaseAPIClient) -> AuthAPI:
    return AuthAPI(api_client)


@pytest.fixture(scope="session")
def booking_api(api_client: BaseAPIClient) -> BookingAPI:
    return BookingAPI(api_client)


@pytest.fixture(scope="session")
def health_check_api(api_client: BaseAPIClient) -> HealthCheckAPI:
    return HealthCheckAPI(api_client)


@pytest.fixture(scope="session")
def auth_token(auth_api: AuthAPI) -> str:
    username, password = get_auth_credentials()
    response = auth_api.create_token(username=username, password=password)

    assert_status_code(response, 200)
    response_json = response.json()
    validate_json_schema(response_json, AUTH_TOKEN_SCHEMA)

    return response_json["token"]


@pytest.fixture()
def sample_booking_payload() -> dict[str, Any]:
    return generate_booking_payload()


@pytest.fixture()
def updated_booking_payload() -> dict[str, Any]:
    return generate_booking_payload(
        {
            "firstname": "Updated",
            "lastname": "Booking",
            "totalprice": 900,
            "depositpaid": False,
            "additionalneeds": "Late checkout",
        }
    )


@pytest.fixture()
def partial_update_payload() -> dict[str, Any]:
    return {
        "firstname": "Partial",
        "lastname": "Update",
    }


@pytest.fixture()
def created_booking(
    booking_api: BookingAPI,
    auth_token: str,
    sample_booking_payload: dict[str, Any],
) -> dict[str, Any]:
    response = booking_api.create_booking(sample_booking_payload)
    assert_status_code(response, 200)

    booking_id = response.json()["bookingid"]
    yield {
        "booking_id": booking_id,
        "payload": sample_booking_payload,
    }

    cleanup_response = booking_api.delete_booking(booking_id, auth_token)
    if cleanup_response.status_code not in (201, 404, 405):
        pytest.fail(
            f"Booking cleanup failed for booking ID {booking_id}. "
            f"Status: {cleanup_response.status_code}. Body: {cleanup_response.text}"
        )


@pytest.fixture(scope="session")
def max_response_time_ms() -> int:
    return get_max_response_time_ms()


@pytest.fixture()
def booking_test_data() -> dict[str, Any]:
    data_path = PROJECT_ROOT / "data" / "booking_payloads.json"
    with data_path.open("r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(autouse=True)
def response_time_guard(request: pytest.FixtureRequest, max_response_time_ms: int) -> None:
    request.node.max_response_time_ms = max_response_time_ms


@pytest.fixture()
def assert_response_performance(max_response_time_ms: int):
    def _assert(response):
        assert_response_time_under(response, max_response_time_ms)

    return _assert
