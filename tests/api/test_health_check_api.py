from __future__ import annotations

import pytest

from api.endpoints.health_check_api import HealthCheckAPI
from utils.assertions import assert_status_code


@pytest.mark.api
@pytest.mark.smoke
def test_health_check_ping_returns_created(
    health_check_api: HealthCheckAPI,
    assert_response_performance,
) -> None:
    response = health_check_api.ping()

    assert_status_code(response, 201)
    assert_response_performance(response)
