import logging
import sys
from typing import Callable, ParamSpec, Any

from collatz_sequence import CollatzSequence
from collatz_analyzer import CollatzAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
log: logging.Logger = logging.getLogger('app')

analyzer = CollatzAnalyzer(1, 100)
best: CollatzSequence = analyzer.longest()
log.info(f"{best.start}: {best.steps} steps, peak: {best.peak}")
P = ParamSpec("P")


def decorator_demo1(function: Callable[P, None]) -> Callable[P, None]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        log.info(f"Before calling the `{function.__name__}` function.")
        function(*args, **kwargs)
        log.info(f"After calling the `{function.__name__}` function.")
    return wrapper


def decorator_demo2(function: Callable[..., None]) -> Callable[..., None]:
    def wrapper(*args: Any, **kwargs: Any) -> None:
        log.info(f"Before calling the `{function.__name__}` function.")
        function(*args, **kwargs)
        log.info(f"After calling the `{function.__name__}` function.")
    return wrapper


@decorator_demo1
def decor_demo1(input: str) -> None:
    log.info(f"Calling decor_demo function with {input} parameter")


@decorator_demo2
def decor_demo2(input: str) -> None:
    log.info(f"Calling decor_demo function with {input} parameter")


decor_demo1("input1")
decor_demo2("input2")
