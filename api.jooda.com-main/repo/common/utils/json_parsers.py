import json


def request_data_to_json(data) -> json:
    try:
        results = json.loads(data.replace("'", '"'))
        return results
    except:
        return data


def find_values_to_json_list(
    json_list: list,
    id_list: list,
    index: int,
    key: str,
    id: str,
    output_keys: list,
) -> tuple:
    def find_list_index(index: int, id: str) -> int:
        if id == json_list[index].get(key, None):
            return index
        return id_list.index(id)

    list_index = find_list_index(index, id)

    return (json_list[list_index].get(key, None) for key in output_keys)
