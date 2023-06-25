import sys
from functools import wraps
from typing import Dict, Type, Optional, Callable, Container, Union


ErrorT = Union[Callable[[Exception], Exception], Type[Exception]]


class ErrorWrapper:
    def __init__(
        self,
        error_mappings: Optional[Dict[Type[Exception], ErrorT]] = None,
        default_error: Optional[ErrorT] = None,
        skipped_errors: Optional[Container[Type[Exception]]] = None,
    ):
        self.error_mappings = error_mappings or {}
        self.default_error = default_error
        self.skipped_errors = {
            *(skipped_errors or set()),
            KeyboardInterrupt,
            SystemExit,
            *self.error_mappings.values(),  # we want to skip all the mapped values as they are already fixed
        }

    def __enter__(self):
        return self

    def is_already_wrapped(self, exc_type: Type[Exception]) -> bool:
        return any(
            issubclass(exc_type, error)
            for error in self.skipped_errors
            if issubclass(error, Exception)
        )

    def create_error(self, original_error: Exception, wrapped_error_type: Type[Exception]):
        _, _, tb = sys.exc_info()
        raise wrapped_error_type(original_error).with_traceback(tb)

    def __exit__(self, exc_type: Type[Exception], exc_val: Exception, exc_tb):
        if exc_val is None:
            return True
        elif self.is_already_wrapped(exc_type):
            return False

        wrapped_error = self.error_mappings.get(exc_type)

        if wrapped_error is not None:
            raise self.create_error(
                original_error=exc_val,
                wrapped_error_type=wrapped_error,
            )
        elif self.default_error is not None:
            raise self.create_error(
                original_error=exc_val,
                wrapped_error_type=self.default_error,
            )

        return False   # No wrapping error was found

    def decorate(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        wrapper: func
        return wrapper

    def __str__(self):
        return f"{type(self).__name__}({self.error_mappings})"


__all__ = ['ErrorWrapper']
