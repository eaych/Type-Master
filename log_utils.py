from functools import wraps
import logging

class LogCalls:
    def __init__(self, level=logging.DEBUG, file='server.log', name=__name__):
        self.name = name
        logging.basicConfig(filename=file, level=level)
        self.logger = logging.getLogger(self.name)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(f"{func.__name__} called")
            if args:
                self.logger.debug(f"{func.__name__}:args:\n{args}")
            if kwargs:
                self.logger.debug(f"{func.__name__}:kwargs:\n{kwargs}")

            result = func(*args, **kwargs)
            self.logger.debug(f"{func.__name__} returned\n{result}")
            return result
        return wrapper