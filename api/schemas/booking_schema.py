BOOKING_SCHEMA = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string", "minLength": 1},
        "lastname": {"type": "string", "minLength": 1},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {"type": "string", "format": "date"},
                "checkout": {"type": "string", "format": "date"},
            },
            "required": ["checkin", "checkout"],
            "additionalProperties": True,
        },
        "additionalneeds": {"type": "string"},
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "additionalProperties": True,
}

CREATE_BOOKING_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_SCHEMA,
    },
    "required": ["bookingid", "booking"],
    "additionalProperties": True,
}

BOOKING_IDS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "bookingid": {"type": "integer"},
        },
        "required": ["bookingid"],
        "additionalProperties": True,
    },
}
