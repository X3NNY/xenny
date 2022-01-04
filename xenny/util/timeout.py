import contextlib
import errno
import os
import signal

DEFAULT_TIMEOUT_MESSAGE = os.strerror(errno.ETIME)

class timeout(contextlib.ContextDecorator):
    def __init__(
        self,
        seconds,
        *,
        timeout_message=DEFAULT_TIMEOUT_MESSAGE,
        suppress_timeout_errors=False,
    ):
        self.seconds = int(seconds)
        self.timeout_message = timeout_message
        self.suppress = bool(suppress_timeout_errors)

    def _timeout_handler(self, signum, frame):
        raise TimeoutError(self.timeout_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)
        if self.suppress and exc_type is TimeoutError:
            return True