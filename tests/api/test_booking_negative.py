from __future__ import annotations

import pytest

from api.endpoints.booking_api import BookingAPI
from utils.assertions import assert_status_code


@pytest.mark.api
@pytest.mark.negative
def test_get_booking_with_invalid_id_returns_not_found(
    booking_api: BookingAPI,
    assert_response_performance,
) -> None:
    response = booking_api.get_booking("999999999")

    assert_status_code(response, 404)
    assert_response_performance(response)


@pytest.mark.api
@pytest.mark.negative
def test_update_booking_without_token_returns_forbidden(
    booking_api: BookingAPI,
    created_booking: dict,
    updated_booking_payload: dict,
    assert_response_performance,
) -> None:
    booking_id = created_booking["booking_id"]
    response = booking_api.update_booking(booking_id, updated_booking_payload, token=None)

    assert_status_code(response, 403)
    assert_response_performance(response)


@pytest.mark.api
@pytest.mark.negative
def test_partial_update_booking_without_token_returns_forbidden(
    booking_api: BookingAPI,
    created_booking: dict,
    partial_update_payload: dict,
    assert_response_performance,
) -> None:
    booking_id = created_booking["booking_id"]
    response = booking_api.partial_update_booking(booking_id, partial_update_payload, token=None)

    assert_status_code(response, 403)
    assert_response_performance(response)


@pytest.mark.api
@pytest.mark.negative
def test_delete_booking_without_token_returns_forbidden(
    booking_api: BookingAPI,
    created_booking: dict,
    assert_response_performance,
) -> None:
    booking_id = created_booking["booking_id"]
    response = booking_api.delete_booking(booking_id, token=None)

    assert_status_code(response, 403)
    assert_response_performance(response)
