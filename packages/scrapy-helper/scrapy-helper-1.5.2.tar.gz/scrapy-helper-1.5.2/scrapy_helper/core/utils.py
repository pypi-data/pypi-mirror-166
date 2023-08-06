import json


def str2list(x, transformer=None):
    """
    convert to list
    :param transformer:
    :param x:
    :return:
    """
    if x is None or isinstance(x, list):
        return x
    try:
        data = json.loads(x)
        if not transformer:
            def transformer(t): return t
        data = list(map(lambda y: transformer(y), data))
        return data
    except:
        return []


def str2dict(v):
    """
    convert str to dict data
    :param v:
    :return:
    """
    try:
        return json.loads(v)
    except:
        return {}


def str2body(v):
    """
    convert str to json data or keep original string
    :param v:
    :return:
    """
    try:
        return json.loads(v)
    except:
        return v