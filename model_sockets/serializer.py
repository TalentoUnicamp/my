import json
import warnings


def filter_unserializable_list(data):
    result = []
    for v in data:
        for option in mapper:
            if isinstance(v, option):
                v = mapper[option](v)
        try:
            json.dumps(v)
            result.append(v)
        except TypeError:
            warnings.warn(f"Type '{type(v)}' is non serializable. Skipping it.")
    return result


def filter_unserializable_dict(data):
    result = {}
    for k, v in data.items():
        for option in mapper:
            if isinstance(v, option):
                v = mapper[option](v)
        try:
            json.dumps(v)
            result[k] = v
        except TypeError:
            warnings.warn(f"Field '{k}' of type '{type(v)}' is non serializable. Skipping it.")

    return result


mapper = {
    list: filter_unserializable_list,
    dict: filter_unserializable_dict
}


def filter_json(content):
    for option in mapper:
        if isinstance(content, option):
            return mapper[option](content)
