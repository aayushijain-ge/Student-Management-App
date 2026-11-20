import time

_store: dict[str, tuple[float, object]] = {}


def get(key: str):
    item = _store.get(key)
    if item is None:
        return None
    expires_at, value = item
    if time.time() > expires_at:      # TTL finished
        del _store[key]
        return None
    return value


def set(key: str, value, ttl: int = 60):
    _store[key] = (time.time() + ttl, value)


def clear_prefix(prefix: str):
    for key in [k for k in _store if k.startswith(prefix)]:
        del _store[key]