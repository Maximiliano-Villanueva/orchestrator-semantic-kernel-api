# Standard imports
import time

from typing import Annotated, Callable, Any, Type

# Internal imports
from app.infrastructure.utils import custom_logs


logger = custom_logs.getLogger("class_annotations")


class MethodObservability(type):
    """
    A metaclass that logs the time elapsed during the execution of methods of the class.
    """
    def __new__(cls, name: Annotated[str, "The name of the class."], bases: Annotated[tuple, "The base classes."], dct: Annotated[dict, "The attribute/method dictionary."]):
        """
        Creates a new instance of the class, modifying its methods to log the execution time.

        Returns:
            Type: The new class with modified methods.
        """
        new_cls = super().__new__(cls, name, bases, dct)
        for attribute_name, attribute in dct.items():
            if callable(attribute):
                setattr(new_cls, attribute_name, cls.wrap_method(attribute))
        return new_cls

    @staticmethod
    def wrap_method(method: Annotated[Callable, "The method to wrap."]) -> Annotated[Callable, "The wrapped method."]:
        """
        Wraps a method to log its execution time.
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = method(*args, **kwargs)
            end_time = time.time()
            logger.info(f"Execution time for {method.__name__}: {end_time - start_time} seconds")
            return result
        return wrapper
