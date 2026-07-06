from __future__ import annotations

import pytest

from api.endpoints.auth_api import AuthAPI
from api.schemas.auth_schema import AUTH_ERROR_SCHEMA, AUTH_TOKEN_SCHEMA
from config.config_loader import get_auth_credentials
from utils.assertions import assert_json_key_exists, assert_status_code
from utils.schema_validator import validate_json_schema


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.contract
def test_create_auth_token_with_valid_credentials(
    auth_api: AuthAPI,
    assert_response_performance,
) -> None:
    username, password = get_auth_credentials()
    response = auth_api.create_token(username=username, password=password)

    assert_status_code(response, 200)
    assert_response_performance(response)

    response_json = response.json()
    validate_json_schema(response_json, AUTH_TOKEN_SCHEMA)
    assert_json_key_exists(response_json, "token")


@pytest.mark.api
@pytest.mark.negative
def test_create_auth_token_with_invalid_credentials_returns_reason(
    auth_api: AuthAPI,
    assert_response_performance,
) -> None:
    response = auth_api.create_token(username="invalid-user", password="invalid-password")

    assert_status_code(response, 200)
    assert_response_performance(response)

    response_json = response.json()
    validate_json_schema(response_json, AUTH_ERROR_SCHEMA)
    assert response_json["reason"] == "Bad credentials"
