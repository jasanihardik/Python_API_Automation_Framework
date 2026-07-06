from __future__ import annotations

import pytest

from api.endpoints.booking_api import BookingAPI
from api.schemas.booking_schema import BOOKING_SCHEMA, CREATE_BOOKING_RESPONSE_SCHEMA
from utils.assertions import assert_json_value, assert_status_code
from utils.schema_validator import validate_json_schema


@pytest.mark.api
@pytest.mark.workflow
@pytest.mark.regression
def test_create_get_update_patch_delete_booking_workflow(
    booking_api: BookingAPI,
    sample_booking_payload: dict,
    updated_booking_payload: dict,
    partial_update_payload: dict,
    auth_token: str,
    assert_response_performance,
) -> None:
    create_response = booking_api.create_booking(sample_booking_payload)
    assert_status_code(create_response, 200)
    assert_response_performance(create_response)

    create_response_json = create_response.json()
    validate_json_schema(create_response_json, CREATE_BOOKING_RESPONSE_SCHEMA)
    booking_id = create_response_json["bookingid"]

    get_response = booking_api.get_booking(booking_id)
    assert_status_code(get_response, 200)
    assert_response_performance(get_response)
    validate_json_schema(get_response.json(), BOOKING_SCHEMA)
    assert_json_value(get_response.json(), "firstname", sample_booking_payload["firstname"])

    update_response = booking_api.update_booking(booking_id, updated_booking_payload, auth_token)
    assert_status_code(update_response, 200)
    assert_response_performance(update_response)
    assert_json_value(update_response.json(), "firstname", updated_booking_payload["firstname"])
    assert_json_value(update_response.json(), "totalprice", updated_booking_payload["totalprice"])

    patch_response = booking_api.partial_update_booking(booking_id, partial_update_payload, auth_token)
    assert_status_code(patch_response, 200)
    assert_response_performance(patch_response)
    assert_json_value(patch_response.json(), "firstname", partial_update_payload["firstname"])
    assert_json_value(patch_response.json(), "lastname", partial_update_payload["lastname"])

    delete_response = booking_api.delete_booking(booking_id, auth_token)
    assert_status_code(delete_response, 201)
    assert_response_performance(delete_response)

    deleted_get_response = booking_api.get_booking(booking_id)
    assert_status_code(deleted_get_response, 404)
