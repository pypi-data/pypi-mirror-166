"""Application implementation - exceptions."""
from {{cookiecutter.package_name}}.app.exceptions.http import (
    HTTPException,
    http_exception_handler,
)


__all__ = ("HTTPException", "http_exception_handler")
