from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta
from typing import Any

from faker import Faker

fake = Faker()


def generate_booking_payload(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=3)

    payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=1500),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
        },
        "additionalneeds": fake.random_element(elements=("Breakfast", "Late checkout", "Airport pickup")),
    }

    if overrides:
        payload = _deep_merge(payload, overrides)

    return payload


def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)

    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value

    return merged
