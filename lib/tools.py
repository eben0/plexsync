import functools
import threading
from threading import Timer
from typing import Callable


def synchronized(wrapped) -> Callable:
    lock = threading.RLock()

    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)

    return _wrapper


class RepeatedTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)