import sys
from functools import wraps
from typing import Dict, Type, Optional, Callable, Container, Union

import pytest


ErrorT = Union[Callable[[Exception], Exception], Type[Exception]]


def create_error(original_error: Exception, wrapped_error_type: Type[Exception]):
    _, _, tb = sys.exc_info()
    raise wrapped_error_type(original_error).with_traceback(tb)


def is_already_wrapped(exc_type: Type[Exception], skipped_errors: Container[Type[Exception]]) -> bool:
    return any(issubclass(exc_type, error) for error in skipped_errors)


def error_wrapper(
    error_mappings: Optional[Dict[Type[Exception], ErrorT]] = None,
    default_error: Optional[ErrorT] = None,
    skipped_errors: Optional[Container[Type[Exception]]] = None,
) -> Callable:
    error_mappings = error_mappings or {}
    skipped_errors = {
        *(skipped_errors or set()),
        KeyboardInterrupt,
        SystemExit,
        *error_mappings.values(),  # we want to skip all the mapped values as they are already fixed
    }

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc_val:
                exc_type = type(exc_val)
                if is_already_wrapped(exc_type, skipped_errors):
                    raise
                wrapped_error = error_mappings.get(exc_type)
                if wrapped_error is not None:
                    create_error(original_error=exc_val, wrapped_error_type=wrapped_error)
                elif default_error is not None:
                    create_error(original_error=exc_val, wrapped_error_type=default_error)
                else:
                    raise
        return inner
    return wrapper


def test_create_error():
    original_error = ValueError("Test error")
    wrapped_error_type = TypeError

    with pytest.raises(wrapped_error_type):
        create_error(original_error, wrapped_error_type)


def test_is_already_wrapped():
    skipped_errors = {KeyboardInterrupt, SystemExit}
    assert is_already_wrapped(KeyboardInterrupt, skipped_errors)
    assert is_already_wrapped(SystemExit, skipped_errors)
    assert is_already_wrapped(TypeError, skipped_errors) == False


def test_error_wrapper_no_wrap():
    @error_wrapper()
    def test_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        test_func()


def test_error_wrapper_default_error():
    @error_wrapper(default_error=TypeError)
    def test_func():
        raise ValueError("Test error")

    with pytest.raises(TypeError):
        test_func()


def test_error_wrapper_mapped_error():
    @error_wrapper(error_mappings={ValueError: TypeError})
    def test_func():
        raise ValueError("Test error")

    with pytest.raises(TypeError):
        test_func()


def test_error_wrapper_skip_errors():
    @error_wrapper(skipped_errors={ValueError})
    def test_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        test_func()

    @error_wrapper(skipped_errors={ValueError})
    def test_func2():
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        test_func2()
