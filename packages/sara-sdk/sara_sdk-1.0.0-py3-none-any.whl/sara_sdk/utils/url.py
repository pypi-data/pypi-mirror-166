from urllib.parse import urlencode as _urlencode


def urlencode(params):
    params = {k: valueToString(v) for k, v in params.items()}
    return "?" + _urlencode(params) if params else ""


def valueToString(value):
    if isinstance(value, (tuple, list, set)):
        return ",".join([valueToString(value) for value in value])
    return str(value)
