from typing import Any, Callable, TypeVar

from noldor import Validator
from noldor import validate as val

P = TypeVar("P")


def validate(*validators: Validator[P]) -> Callable[[Any, Any, P], None]:
    return lambda _, __, value: val(value, *validators)
