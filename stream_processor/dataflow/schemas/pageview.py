SCHEMA_PAGEVIEW = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "PageView",
    "type": "object",
    "required": ["user_id", "postcode", "webpage", "timestamp"],
    "properties": {
        "user_id": {
            "title": "User_id",
            "type": "integer",
            "examples": [1234],
            "default": 0,
        },
        "postcode": {
            "title": "Postcode",
            "type": "string",
            "default": "",
            "examples": ["SW19"],
            "pattern": "^.*$",
        },
        "webpage": {
            "title": "Webpage",
            "type": "string",
            "default": "",
            "examples": ["www.website.com/index.html"],
            "pattern": "^.*$",
        },
        "timestamp": {
            "title": "Timestamp",
            "type": "integer",
            "examples": [1611662684],
            "default": 0,
        },
    },
}
