""" A logger for use within Decision Engine presets in SDVI Rally. """
import functools
import logging
import sys
from presets.local.ae_environment import LOG_LEVEL
from typing import Callable, Any


class CallCounted:
    """
    A decorator class that counts the number of times a method is called.

    Attributes:
        method (Callable[..., Any]): The method to be decorated.
        counter (int): The call count.
    """

    def __init__(self, method: Callable[..., Any]) -> None:
        """
        Initializes the CallCounted instance.

        Args:
            method (Callable[..., Any]): The method to be decorated.
        """
        self.method = method
        self.counter = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Increments the call count and calls the decorated method.

        Args:
            *args (Any): Positional arguments for the method.
            **kwargs (Any): Keyword arguments for the method.

        Returns:
            Any: The result of the method call.
        """
        self.counter += 1
        return self.method(*args, **kwargs)


class RallyLogger:
    """
    A singleton logger class for SDVI Rally.

    Attributes:
        instance (RallyLogger): The singleton instance.
        _loggers (dict): A dictionary of loggers.
    """

    def __new__(cls) -> 'RallyLogger':
        """
        Creates a new instance if one does not exist, otherwise returns the existing instance.

        Returns:
            RallyLogger: The singleton instance.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    @property
    def logger(self) -> logging.Logger:
        """
        Returns the base logger, initializing it if necessary.

        Returns:
            logging.Logger: The base logger.
        """
        if not hasattr(self, '_loggers'):
            self._loggers = {}
        if 'base' not in self._loggers:
            self._loggers['base'] = self.init_logger('base')
        return self._loggers['base']

    def get_logger(self, name: str = 'base', level: int = LOG_LEVEL) -> logging.Logger:
        """
        Returns a logger with the specified name and level, initializing it if necessary.

        Args:
            name (str): The name of the logger.
            level (int): The logging level.

        Returns:
            logging.Logger: The logger.
        """
        if not hasattr(self, '_loggers'):
            self._loggers = {}
        if name not in self._loggers:
            self._loggers[name] = self.init_logger(name, level)
        return self._loggers[name]

    def init_logger(self, name: str, level: int = LOG_LEVEL) -> logging.Logger:
        """
        Initializes a logger with the specified name and level.

        Args:
            name (str): The name of the logger.
            level (int): The logging level.

        Returns:
            logging.Logger: The initialized logger.
        """
        logger = logging.getLogger(name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

        for level_name in ['debug', 'info', 'warning', 'error', 'critical']:
            setattr(logger, level_name, CallCounted(getattr(logger, level_name)))
        logger.details = self.details

        if name == 'base':
            import rally
            logger.info(f'Rally SDK Version {rally.__version__}')
        return logger

    def details(self) -> None:
        """
        Logs the count of different log levels.

        Returns:
            None
        """
        msg = f'Infos: {self.logger.info.counter} Warnings: {self.logger.warning.counter} Errors: {self.logger.error.counter} Criticals: {self.logger.critical.counter}'
        self.logger.info(msg)


def log(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    A decorator that logs the context and details of a function call.

    Args:
        func (Callable[[Any], Any]): The function to be decorated.

    Returns:
        Callable[[Any], Any]: The decorated function.
    """

    def inner(context: Any) -> Any:
        """
        Logs the context before and details after the function call.

        Args:
            context (Any): The context to be logged.

        Returns:
            Any: The result of the function call.
        """
        logger = RallyLogger().logger
        logger.info(context)
        result = func(context)
        logger.details()
        return result

    return inner
