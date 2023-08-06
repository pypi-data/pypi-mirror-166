from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from noldor import Response

P = TypeVar("P")

RESPECTED = "[green]RESPECTED[/green]"
NOT_RESPECTED = "[red]NOT RESPECTED[/red]"


# TODO For some reasons, adding "slots=True" here brakes everything.
@dataclass(frozen=True)
class Validator(Generic[P]):

    condition: Callable[[P], bool]
    message: str

    def __call__(self, p: P) -> Response:
        result = self.condition(p)
        if result is True:
            log = [f"{RESPECTED}: {p} {self.message}"]
        else:
            log = [f"{NOT_RESPECTED}: {p} {self.message}"]
        return Response(result, log)
