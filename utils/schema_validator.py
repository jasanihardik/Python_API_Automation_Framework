from __future__ import annotations

from typing import Any

from jsonschema import ValidationError, validate


def validate_json_schema(instance: Any, schema: dict[str, Any]) -> None:
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as error:
        raise AssertionError(f"Schema validation failed: {error.message}") from error
