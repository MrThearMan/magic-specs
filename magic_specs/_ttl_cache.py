from copy import deepcopy
from functools import wraps
from time import monotonic
from typing import Any, Callable, ParamSpec, TypeVar, Union

T = TypeVar("T")
P = ParamSpec("P")

__all__ = [
    "ttl_cache",
]


def ttl_cache(ttl: int = 2):
    """
    Cache decorated function's return value for the given number of seconds.
    This can be useful when the result of the function might change with time,
    and we would otherwise need to make a local variable to "cache" that value.

    Note that the cached value is not shared between workers/processes, but can
    be valid for a second request to the same worker/process if the ttl is long enough!
    """

    _sentinel = object()
    _cache: Any = _sentinel
    _set: Union[float, object] = _sentinel

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            nonlocal _cache, _set
            _now = monotonic()
            if _cache is not _sentinel and _set is not _sentinel and _now - _set < ttl:
                return _cache
            _cache = func(*args, **kwargs)
            _set = monotonic()
            return deepcopy(_cache)

        return wrapper

    # Called without parenthesis, ttl is the decorated function
    if callable(ttl):
        _func = ttl
        ttl = 2
        return decorator(_func)

    return decorator
