import pytest

from typing import List
from assimilator.core.patterns.lazy_command import LazyCommand


def test_lazy_command_no_args():
    def test_func() -> int:
        return 42

    lazy_result = LazyCommand(test_func)
    assert isinstance(lazy_result, LazyCommand)
    assert lazy_result() == 42


def test_lazy_command_with_args():
    def test_func(a: int, b: int) -> int:
        return a * b

    lazy_result = LazyCommand(test_func, 6, 7)
    assert isinstance(lazy_result, LazyCommand)
    assert lazy_result() == 42


def test_lazy_command_with_kwargs():
    def test_func(a: int, b: int) -> int:
        return a * b

    lazy_result = LazyCommand(test_func, a=6, b=7)
    assert isinstance(lazy_result, LazyCommand)
    assert lazy_result() == 42


def test_lazy_command_eq():
    def test_func(a: int, b: int) -> int:
        return a * b

    lazy_result_1 = LazyCommand(test_func, 6, 7)
    lazy_result_2 = LazyCommand(test_func, 6, 7)
    assert lazy_result_1 == lazy_result_2


def test_lazy_command_gt():
    def test_func(a: int, b: int) -> int:
        return a * b

    lazy_result = LazyCommand(test_func, 6, 7)
    assert lazy_result > 40


def test_lazy_command_getattr():
    class TestClass:
        def __init__(self):
            self.value = 42

        def get_value(self) -> int:
            return self.value

    lazy_result = LazyCommand(TestClass)
    assert lazy_result.get_value() == 42
    assert lazy_result.value == 42


def test_lazy_command_bool():
    def test_func(a: List[int]) -> bool:
        return bool(a)

    lazy_result_true = LazyCommand(test_func, [1, 2, 3])
    assert lazy_result_true

    lazy_result_false = LazyCommand(test_func, [])
    assert not lazy_result_false


def test_lazy_command_decorate():
    @LazyCommand.decorate
    def test_func(a: int, b: int, lazy: bool = False) -> int:   # TODO: fix lazy argument
        return a * b

    lazy_result = test_func(a=6, b=7, lazy=True)
    assert isinstance(lazy_result, LazyCommand)
    assert lazy_result() == 42
