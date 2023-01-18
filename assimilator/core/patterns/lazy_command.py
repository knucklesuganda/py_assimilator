from typing import Union, Callable, Iterable, Container, TypeVar, Generic, Iterator

T = TypeVar("T")


class LazyCommand(Generic[T]):
    def __init__(self, command: Callable, *args, **kwargs):
        self.command = command
        self.args = args
        self.kwargs = kwargs
        self._results: T = None

    def __call__(self) -> Union[Container[T], T]:
        if self._results is not None:
            return self._results

        self._results = self.command(*self.args, **self.kwargs)
        return self._results

    def __iter__(self) -> Iterator[T]:
        results = self()

        if not isinstance(results, Iterable):  # get() command
            raise StopIteration("Results are not iterable")

        return iter(results)  # filter() command

    def __bool__(self):
        return bool(self())

    def __str__(self):
        return f"Lazy<{self.command}(*{self.args}, **{self.kwargs})>"

    def __repr__(self):
        return str(self)


__all__ = ['LazyCommand']
