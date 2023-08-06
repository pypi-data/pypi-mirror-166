from functools import reduce
from operator import add

from noldor import Response, Validator
from noldor._typevar import P


def check(parameter: P, *validators: Validator[P]) -> Response:
    """Check parameter p against the given validators.

    If the result of a validation response is False, everything is False.
    """
    responses = map(lambda v: v(parameter), validators)
    return reduce(add, responses)


def validate(parameter: P, *validators: Validator[P]) -> None:
    """Check parameter p against the given validators.

    If the result of a validation response is False, an Exception is raised.
    """
    res = check(parameter, *validators)
    if res.result is False:
        raise ValueError(res.log)
