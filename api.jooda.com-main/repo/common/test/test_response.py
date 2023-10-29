import json

ESCAPE_CHAR = "ESCAPE_CHAR"


def get_content_from_response(response):
    response = json.loads(response.content.decode("utf-8"))
    if response["success"]:
        keys = list(response["payload"].keys())

        return response["payload"] if len(keys) != 1 else response["payload"][keys[0]]
    else:
        return response["error_code"]


def check_payload_validate_value(serializer_class, response):
    get_serializer_fields = lambda serializer_class: list(
        serializer_class().get_fields()
    )

    payload = get_content_from_response(response)
    payload_type = type(payload)

    if payload_type == dict and payload.get("total_count", None):
        payload = payload["results"][0]
    if payload_type == list and len(payload) != 0:
        payload = payload[0]
    for field in get_serializer_fields(serializer_class):
        if payload_type == dict and payload.get(field, ESCAPE_CHAR) is ESCAPE_CHAR:
            print(payload.get(field, None))
            return False
    return True
