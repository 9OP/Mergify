from abc import ABC
from fastapi import HTTPException, status, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def setup_exception_handlers(app: FastAPI):
    # Handles app, fastapi, starlette errors
    app.add_exception_handler(
        StarletteHTTPException,
        make_exception_handler(status.HTTP_400_BAD_REQUEST),
    )

    # Handles global errors
    app.add_exception_handler(
        Exception,
        make_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR),
    )


def make_exception_handler(default_status: int):
    def exception_handler(req: Request, exc: StarletteHTTPException):
        status_code = getattr(exc, "status_code", default_status)
        content = {
            "code": status_code,
            "detail": getattr(exc, "detail", str(exc).replace("\n", " ")),
        }
        compacted_content = {k: v for k, v in content.items() if v is not None}
        return JSONResponse(
            status_code=status_code,
            headers=getattr(exc, "headers", {}),
            content=compacted_content,
        )

    return exception_handler


class ApiResponse(HTTPException, ABC):
    """Common base class for API errors"""

    def __init__(
        self,
        status_code: int,
        detail=None,
        headers=None,
        **kwargs,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
            **kwargs,
        )


class AuthError(ApiResponse):
    def __init__(self, detail="Authentication error", **kwargs):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, **kwargs)


class GithubError(ApiResponse):
    def __init__(self, status: int, detail: str, **kwargs):
        super().__init__(status, f"GITHUB ERROR: {detail}", **kwargs)
