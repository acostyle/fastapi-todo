import json
import logging
import time
from collections.abc import Callable
from uuid import uuid4

from fastapi import Request, Response
from starlette.responses import JSONResponse

MAX_LOG_BYTES = 4_000
SENSITIVE_KEYS = {
    "password",
    "current_password",
    "new_password",
}

logger = logging.getLogger("app.middleware")

SUSPICIOUS_USER_AGENT_KEYWORDS = {
    "curl",
    "postmanruntime",
}


def _mask_request_json(request_body: bytes) -> str:
    if not request_body:
        return ""
    try:
        payload = json.loads(request_body[:MAX_LOG_BYTES])
    except (json.JSONDecodeError, UnicodeDecodeError):
        return ""

    if not isinstance(payload, dict):
        return ""

    masked_payload = {}
    for key, value in payload.items():
        if key.casefold() in SENSITIVE_KEYS:
            masked_payload[key] = "***"
        else:
            masked_payload[key] = value
    return json.dumps(masked_payload, ensure_ascii=True)


async def log_request_response(request: Request, call_next: Callable) -> Response:
    start = time.perf_counter()
    request_id = request.headers.get("x-request-id") or str(uuid4())

    req_body = await request.body()

    try:
        response = await call_next(request)
    except Exception:
        duration = time.perf_counter() - start
        logger.exception(
            "[%s] %s %s -> unhandled exception (%.4fs)",
            request_id,
            request.method,
            request.url.path,
            duration,
        )
        raise

    duration = time.perf_counter() - start
    request_json = _mask_request_json(req_body)

    logger.info(
        "[%s] %s %s -> %s (%.4fs)",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )
    if request.url.query:
        logger.info("[%s] Query: %s", request_id, request.url.query)
    if request_json:
        logger.info("[%s] Request json: %s", request_id, request_json)

    if "x-request-id" not in response.headers:
        response.headers["x-request-id"] = request_id

    return response


def _is_suspicious_user_agent(user_agent: str) -> bool:
    ua = user_agent.casefold()
    return any(keyword in ua for keyword in SUSPICIOUS_USER_AGENT_KEYWORDS)


async def block_suspicious_user_agents(
    request: Request, call_next: Callable
) -> Response:
    user_agent = request.headers.get("user-agent")
    if user_agent and _is_suspicious_user_agent(user_agent):
        return JSONResponse(
            status_code=403,
            content={"detail": "User-Agent is not allowed"},
        )

    return await call_next(request)
