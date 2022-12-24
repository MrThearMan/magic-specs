import re
from collections import OrderedDict, defaultdict, deque
from typing import NamedTuple, Sequence, TypeVar

import pytest

from magic_specs import batched

T = TypeVar("T")


class BatchGenArgs(NamedTuple):
    array: Sequence[T]
    batch_size: int
    batches: Sequence[Sequence[T]]


@pytest.mark.parametrize(
    ["array", "batch_size", "batches"],
    [
        BatchGenArgs(
            array=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            batch_size=1,
            batches=[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]],
        ),
        BatchGenArgs(
            array=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            batch_size=2,
            batches=[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]],
        ),
        BatchGenArgs(
            array=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            batch_size=3,
            batches=[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]],
        ),
        BatchGenArgs(
            array=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            batch_size=10,
            batches=[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
        ),
        BatchGenArgs(
            array=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            batch_size=11,
            batches=[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
        ),
        BatchGenArgs(
            array=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            batch_size=3,
            batches=[(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)],
        ),
        BatchGenArgs(
            array={0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""},
            batch_size=3,
            batches=[{0: "", 1: "", 2: ""}, {3: "", 4: "", 5: ""}, {6: "", 7: "", 8: ""}, {9: ""}],
        ),
        BatchGenArgs(
            array={0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}.keys(),
            batch_size=3,
            batches=[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]],
        ),
        BatchGenArgs(
            array={0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}.values(),
            batch_size=3,
            batches=[["", "", ""], ["", "", ""], ["", "", ""], [""]],
        ),
        BatchGenArgs(
            array=range(10),
            batch_size=3,
            batches=[range(0, 3), range(3, 6), range(6, 9), range(9, 10)],
        ),
        BatchGenArgs(
            array=OrderedDict({0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}),
            batch_size=3,
            batches=[
                OrderedDict({0: "", 1: "", 2: ""}),
                OrderedDict({3: "", 4: "", 5: ""}),
                OrderedDict({6: "", 7: "", 8: ""}),
                OrderedDict({9: ""}),
            ],
        ),
        BatchGenArgs(
            array=defaultdict(
                **{"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": ""}
            ),
            batch_size=3,
            batches=[
                defaultdict(**{"0": "", "1": "", "2": ""}),
                defaultdict(**{"3": "", "4": "", "5": ""}),
                defaultdict(**{"6": "", "7": "", "8": ""}),
                defaultdict(**{"9": ""}),
            ],
        ),
        BatchGenArgs(
            array=deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
            batch_size=3,
            batches=[deque([0, 1, 2]), deque([3, 4, 5]), deque([6, 7, 8]), deque([9])],
        ),
    ],
    ids=[
        "Batch size 1",
        "Batch size 2",
        "Batch size 3",
        "Batch size max",
        "Batch size over",
        "Tuple",
        "Dict",
        "DictKeys",
        "DictValues",
        "Range",
        "OrderedDict",
        "defaultdict",
        "deque",
    ],
)
def test_batched(array: Sequence[T], batch_size: int, batches: Sequence[Sequence[T]]):
    batches = iter(batches)
    for batch in batched(array, batch_size=batch_size):
        assert batch == next(batches)


def test_batched__negative_batch_size():
    with pytest.raises(ValueError, match=re.escape("Batch size must be positive.")):
        for _ in batched([1, 2, 3], batch_size=-1):
            pass
