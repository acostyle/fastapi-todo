from fastapi import Request
from fastapi.responses import JSONResponse

from src.users.exceptions import UserError


async def user_exception_handler(request: Request, exc: UserError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
    )
