from dataclasses import dataclass
from typing import TypeVar

Self = TypeVar("Self", bound="Response")


@dataclass(frozen=True, slots=True)
class Response:

    result: bool
    log: list[str]

    def __add__(self: Self, other: Self) -> Self:
        result = self.result and other.result
        log = self.log + other.log
        return Response(result, log)
