from collections.abc import Mapping


def deep_merge(d, u):
    """ Exactly like dict.update(), but deep.
    """
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = deep_merge(d.get(k, {}), v)
        else:
            d[k] = v
    return d
