import logging
import sys
from typing import Callable, Any


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
log: logging.Logger = logging.getLogger('app')


def decorator_demo_with_params(logging: bool) -> Callable[..., Callable[..., Any]]:
    def decorator(function: Callable[..., None]) -> Callable[..., Any]:
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]):
            if logging:
                log.info(f"Before calling the `{function.__name__}` function with parameter")
            result: Any = function(*args, **kwargs)
            if logging:
                log.info(f"Before calling the `{function.__name__}` function with parameter, result: `{result}`.")
            return result
        return wrapper
    return decorator


class DecoratorDemo:
    @decorator_demo_with_params(logging=True)
    def decor_demo_with_params_logging(self, input: str) -> str:
        log.info(f"Calling decor_demo_with_params_logging with params function with logging, input: `{input}`.")
        return input

    @decorator_demo_with_params(logging=False)
    def decor_demo_with_params_without_logging(self, input: str) -> str:
        log.info(
            f"Calling decor_demo_with_params_without_logging with params function without logging, input: `{input}`.")
        return input

    def decorator_caller(self, logging: bool, input: str):
        decorator_demo_with_params(logging)(self.decor_demo_with_params_logging)(input)


decorator_params = DecoratorDemo()
decorator_params.decor_demo_with_params_logging("input1")
print("---")
decorator_params.decor_demo_with_params_without_logging("input2")
print("---")
decorator_params.decorator_caller(logging=True, input="input3")
