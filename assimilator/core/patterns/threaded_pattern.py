from abc import abstractmethod
from threading import Thread
from typing import Optional

from core.patterns import StartCloseContextMixin


class ThreadedPattern(StartCloseContextMixin):
    def __init__(self):
        super(ThreadedPattern, self).__init__()
        self.is_running: bool = False
        self._thread: Optional[Thread] = None

    @abstractmethod
    def run(self):
        raise NotImplementedError(f"run() must be implemented in {self.__class__.__name__}")

    def stop(self):
        self.is_running = False

        if self._thread is not None:
            self._thread.join()

    def start(self, threaded: bool = False):
        self.is_running = True

        if threaded:
            self._thread = Thread(target=self.run)
            self._thread.start()
        else:
            self.run()
