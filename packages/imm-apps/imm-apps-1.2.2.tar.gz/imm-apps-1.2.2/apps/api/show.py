from pydantic import ValidationError
from fastapi import HTTPException


def print_validation_error(e: ValidationError):
    error_msg = ""
    for err in e.errors():
        loc = "->".join(err["loc"]) + ": "
        msg = err["msg"]
        error_msg += loc + msg + "\n"
    return error_msg


def show_exception(e: Exception):
    if type(e) == ValidationError:
        raise HTTPException(status_code=422, detail=print_validation_error(e))
    else:
        raise HTTPException(status_code=422, detail=e)
