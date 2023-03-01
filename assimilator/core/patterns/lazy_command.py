from functools import wraps
from typing import Union, Callable, Iterable, TypeVar, Generic, Iterator

T = TypeVar("T")


class LazyCommand(Generic[T]):
    def __init__(self, command: Callable, *args, **kwargs):
        self.command = command
        self.args = args
        self.kwargs = kwargs
        self._results: T = None

    def __call__(self) -> Union[T]:
        if self._results is not None:
            return self._results

        self._results = self.command(*self.args, **self.kwargs)
        return self._results

    def __iter__(self) -> Iterator[T]:
        results = self()

        if not isinstance(results, Iterable):  # get() command
            raise StopIteration("Results are not iterable")

        return iter(results)  # filter() command

    def __eq__(self, other):
        return self() == other

    def __gt__(self, other):
        return self() > other

    def __getattr__(self, item):
        result = self()
        return getattr(result, item)

    def __bool__(self):
        return bool(self())

    def __str__(self):
        return f"Lazy<{self.command}(*{self.args}, **{self.kwargs})>"

    def __repr__(self):
        return str(self)

    @staticmethod
    def decorate(func: Callable) -> Callable:

        @wraps(func)
        def lazy_wrapper(*args, lazy: bool = False, **kwargs) -> Union[LazyCommand[T], T]:
            if lazy:
                return LazyCommand(
                    func,
                    *args,
                    lazy=False,
                    **kwargs,
                )

            return func(*args, **kwargs)

        lazy_wrapper: func
        return lazy_wrapper


__all__ = ['LazyCommand']
