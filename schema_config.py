schema = {
    "message": {
        "type": "dict",
        "require_all": True,
        "schema": {"up": {"type": "string"}, "down": {"type": "string"}},
    },
    "notifiers": {
        "type": "dict",
        "valueschema": {
            "type": "dict",
            "schema": {
                "address": {"type": "string", "required": True},
                "sites": {"type": "list", "required": True},
                "messageDataName": {"type": "string", "required": True},
                "data": {"type": "dict"},
            },
        },
    },
    "sites": {
        "type": "dict",
        "valueschema": {
            "type": "dict",
            "require_all": True,
            "allow_unknown": True,
            "schema": {
                "address": {"type": "string"},
                "consider_up": {"type": "list", "schema": {"type": "integer"}},
            },
        },
    },
}
