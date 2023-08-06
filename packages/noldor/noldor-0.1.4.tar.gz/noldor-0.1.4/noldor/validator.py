from dataclasses import dataclass
from typing import Callable, Generic

from noldor import Response
from noldor._typevar import P

RESPECTED = "[green]RESPECTED[/green]"
NOT_RESPECTED = "[red]NOT RESPECTED[/red]"


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=True,
    match_args=False,
    kw_only=False,
    slots=False,  # TODO "slots=True" brakes everything. See: https://github.com/python/cpython/issues/90562
)
class Validator(Generic[P]):

    __slots__ = ("condition", "message")

    condition: Callable[[P], bool]
    message: str

    def __call__(self, p: P) -> Response:
        result = self.condition(p)
        if result is True:
            log = f"{RESPECTED}: {p} {self.message}"
        else:
            log = f"{NOT_RESPECTED}: {p} {self.message}"
        return Response(result, log)
