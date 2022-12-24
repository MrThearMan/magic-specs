# ruff: noqa
from enum import Enum, unique
from time import perf_counter

import pytest
from bidict import bidict

from magic_specs import Definition


@pytest.mark.benchmark
def test_benchmark():
    start = perf_counter()

    for _ in range(100_000):

        class TestEnum(Enum):
            A = 1
            B = 2
            C = 4

    interval1 = perf_counter()

    for _ in range(100_000):
        test_bidict = bidict(A=1, B=2, C=3)

    interval2 = perf_counter()

    for _ in range(100_000):

        class TestEnum(Definition, unique=False):
            A = 1
            B = 2
            C = 4

    end = perf_counter()

    print(f"Enum: {interval1 - start:.2} s.")
    print(f"bidict: {interval2 - interval1:.2} s.")
    print(f"Definition: {end - interval2:.2} s.")


@pytest.mark.benchmark
def test_benchmark__unique():
    start = perf_counter()

    for _ in range(100_000):

        @unique
        class TestEnum(Enum):
            A = 1
            B = 2
            C = 4

    interval1 = perf_counter()

    for _ in range(100_000):
        test_bidict = bidict(A=1, B=2, C=3)

    interval2 = perf_counter()

    for _ in range(100_000):

        class TestEnum(Definition):
            A = 1
            B = 2
            C = 4

    end = perf_counter()

    print(f"Enum: {interval1 - start:.2} s.")
    print(f"bidict: {interval2 - interval1:.2} s.")
    print(f"Definition: {end - interval2:.2} s.")
