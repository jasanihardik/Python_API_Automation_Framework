AUTH_TOKEN_SCHEMA = {
    "type": "object",
    "properties": {
        "token": {"type": "string", "minLength": 1},
    },
    "required": ["token"],
    "additionalProperties": True,
}

AUTH_ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string", "minLength": 1},
    },
    "required": ["reason"],
    "additionalProperties": True,
}
