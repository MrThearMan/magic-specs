from itertools import islice
from typing import Any, Generator, KeysView, Mapping, Sequence, TypeVar, ValuesView

__all__ = [
    "batched",
]


T = TypeVar("T", Sequence, Mapping, KeysView, ValuesView)


def batched(iterable: T, batch_size: int) -> Generator[T, Any, None]:
    if batch_size <= 0:
        msg = "Batch size must be positive."
        raise ValueError(msg)

    while iterable:
        try:
            iterable, batch = iterable[batch_size:], iterable[:batch_size]

        except (TypeError, KeyError):
            if isinstance(iterable, Mapping):
                try:
                    iterable, batch = (
                        iterable.__class__(islice(iterable.items(), batch_size, len(iterable))),
                        iterable.__class__(islice(iterable.items(), 0, batch_size)),
                    )
                except (TypeError, KeyError):
                    iterable, batch = (
                        iterable.__class__(**dict(islice(iterable.items(), batch_size, len(iterable)))),
                        iterable.__class__(**dict(islice(iterable.items(), 0, batch_size))),
                    )
            else:
                try:
                    iterable, batch = (
                        iterable.__class__(islice(iter(iterable), batch_size, len(iterable))),
                        iterable.__class__(islice(iter(iterable), 0, batch_size)),
                    )
                except (TypeError, KeyError):
                    iterable, batch = (
                        list(islice(iter(iterable), batch_size, len(iterable))),
                        list(islice(iter(iterable), 0, batch_size)),
                    )

        yield batch
