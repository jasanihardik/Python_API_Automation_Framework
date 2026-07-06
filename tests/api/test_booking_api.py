from __future__ import annotations

import pytest

from api.endpoints.booking_api import BookingAPI
from api.schemas.booking_schema import (
    BOOKING_IDS_SCHEMA,
    BOOKING_SCHEMA,
    CREATE_BOOKING_RESPONSE_SCHEMA,
)
from utils.assertions import assert_json_value, assert_status_code
from utils.schema_validator import validate_json_schema


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.contract
def test_get_booking_ids_returns_list(
    booking_api: BookingAPI,
    assert_response_performance,
) -> None:
    response = booking_api.get_booking_ids()

    assert_status_code(response, 200)
    assert_response_performance(response)
    validate_json_schema(response.json(), BOOKING_IDS_SCHEMA)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.contract
def test_create_booking_returns_booking_id_and_booking_details(
    booking_api: BookingAPI,
    sample_booking_payload: dict,
    auth_token: str,
    assert_response_performance,
) -> None:
    response = booking_api.create_booking(sample_booking_payload)

    assert_status_code(response, 200)
    assert_response_performance(response)

    response_json = response.json()
    validate_json_schema(response_json, CREATE_BOOKING_RESPONSE_SCHEMA)
    assert response_json["booking"]["firstname"] == sample_booking_payload["firstname"]
    assert response_json["booking"]["lastname"] == sample_booking_payload["lastname"]

    booking_api.delete_booking(response_json["bookingid"], auth_token)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.contract
def test_get_created_booking_by_id(
    booking_api: BookingAPI,
    created_booking: dict,
    assert_response_performance,
) -> None:
    booking_id = created_booking["booking_id"]
    response = booking_api.get_booking(booking_id)

    assert_status_code(response, 200)
    assert_response_performance(response)

    response_json = response.json()
    validate_json_schema(response_json, BOOKING_SCHEMA)
    assert_json_value(response_json, "firstname", created_booking["payload"]["firstname"])
    assert_json_value(response_json, "lastname", created_booking["payload"]["lastname"])


@pytest.mark.api
@pytest.mark.regression
def test_update_booking_with_valid_token(
    booking_api: BookingAPI,
    created_booking: dict,
    updated_booking_payload: dict,
    auth_token: str,
    assert_response_performance,
) -> None:
    booking_id = created_booking["booking_id"]
    response = booking_api.update_booking(booking_id, updated_booking_payload, auth_token)

    assert_status_code(response, 200)
    assert_response_performance(response)

    response_json = response.json()
    validate_json_schema(response_json, BOOKING_SCHEMA)
    assert_json_value(response_json, "firstname", updated_booking_payload["firstname"])
    assert_json_value(response_json, "lastname", updated_booking_payload["lastname"])
    assert_json_value(response_json, "totalprice", updated_booking_payload["totalprice"])


@pytest.mark.api
@pytest.mark.regression
def test_partial_update_booking_with_valid_token(
    booking_api: BookingAPI,
    created_booking: dict,
    partial_update_payload: dict,
    auth_token: str,
    assert_response_performance,
) -> None:
    booking_id = created_booking["booking_id"]
    response = booking_api.partial_update_booking(booking_id, partial_update_payload, auth_token)

    assert_status_code(response, 200)
    assert_response_performance(response)

    response_json = response.json()
    validate_json_schema(response_json, BOOKING_SCHEMA)
    assert_json_value(response_json, "firstname", partial_update_payload["firstname"])
    assert_json_value(response_json, "lastname", partial_update_payload["lastname"])


@pytest.mark.api
@pytest.mark.regression
def test_delete_booking_with_valid_token(
    booking_api: BookingAPI,
    sample_booking_payload: dict,
    auth_token: str,
    assert_response_performance,
) -> None:
    create_response = booking_api.create_booking(sample_booking_payload)
    assert_status_code(create_response, 200)

    booking_id = create_response.json()["bookingid"]
    delete_response = booking_api.delete_booking(booking_id, auth_token)

    assert_status_code(delete_response, 201)
    assert_response_performance(delete_response)

    get_response = booking_api.get_booking(booking_id)
    assert_status_code(get_response, 404)
