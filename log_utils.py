from functools import wraps
from time import asctime
import logging

class LogCalls:
    def __init__(self, level=logging.DEBUG, file='server.log', name=__name__, prefix=""):
        self.prefix = prefix + ":" if prefix else ""
        self.name = name
        logging.basicConfig(filename=file, level=level)
        self.logger = logging.getLogger(self.name)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(f"{self.prefix}{func.__name__} called ({asctime()})")
            if args:
                self.logger.debug(f"{self.prefix}{func.__name__}:args:\n{args}")
            if kwargs:
                self.logger.debug(f"{self.prefix}{func.__name__}:kwargs:\n{kwargs}")

            result = func(*args, **kwargs)
            self.logger.debug(f"{self.prefix}{func.__name__}:returned\n{result}")
            return result
        return wrapper