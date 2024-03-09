from typing import Any

from fastapi import HTTPException


def raise_exception_if_true(
        item: Any,
        on_error_message: str,
        status_code: int,
        **kwargs,
) -> bool:
    """
    Validates that the `expression` argument's bool cast equals to the `True`.
    If so, raises an HTTPException with the specified status code and error message.
    All keyword arguments will be passed to the exception.
    """
    if bool(item):
        raise HTTPException(
            detail=on_error_message,
            status_code=status_code,
            **kwargs
        )
    return True
