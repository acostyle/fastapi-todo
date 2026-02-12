from fastapi import Request
from fastapi.responses import JSONResponse

from src.tasks.exceptions import TaskError


async def task_exception_handler(request: Request, exc: TaskError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
    )
