from abc import ABC, abstractmethod


class StartCloseContextMixin(ABC):
    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError("close() is not implemented")

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError("start() is not implemented")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

        if exc_type is not None:
            raise exc_val
