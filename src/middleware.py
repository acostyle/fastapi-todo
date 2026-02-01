import json
import logging
import time
from typing import Any, Callable
from uuid import uuid4

from fastapi import Request, Response
from starlette.responses import JSONResponse, Response as StarletteResponse

MAX_LOG_BYTES = 10_000
SENSITIVE_KEYS = {
    "password",
    "current_password",
    "new_password",
    "token",
    "access_token",
    "refresh_token",
    "secret",
}

logger = logging.getLogger("app.middleware")

SUSPICIOUS_USER_AGENT_KEYWORDS = {
    "curl",
    "postmanruntime",
}


def _safe_decode(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def _mask_sensitive(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {
            key: ("***" if key in SENSITIVE_KEYS else _mask_sensitive(value))
            for key, value in obj.items()
        }
    if isinstance(obj, list):
        return [_mask_sensitive(item) for item in obj]
    return obj


def _format_body(body: bytes, content_type: str | None) -> str:
    if not body:
        return ""

    content_type = (content_type or "").lower()
    if "application/json" in content_type:
        try:
            parsed = json.loads(body)
            masked = _mask_sensitive(parsed)
            return json.dumps(masked, ensure_ascii=True)
        except json.JSONDecodeError:
            return _safe_decode(body[:MAX_LOG_BYTES])

    if content_type.startswith("text/") or "application/x-www-form-urlencoded" in content_type:
        return _safe_decode(body[:MAX_LOG_BYTES])

    return f"<{len(body)} bytes, content-type={content_type or 'unknown'}>"


async def log_request_response(request: Request, call_next: Callable) -> Response:
    start = time.perf_counter()
    request_id = request.headers.get("x-request-id") or str(uuid4())

    req_body = await request.body()
    req_body_text = _format_body(req_body[:MAX_LOG_BYTES], request.headers.get("content-type"))

    response = await call_next(request)

    resp_body = b""
    async for chunk in response.body_iterator:
        resp_body += chunk
    resp_body_text = _format_body(resp_body[:MAX_LOG_BYTES], response.media_type)

    duration = time.perf_counter() - start

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
    if req_body_text:
        logger.info("[%s] Request body: %s", request_id, req_body_text)
    if resp_body_text:
        logger.info("[%s] Response body: %s", request_id, resp_body_text)

    return StarletteResponse(
        content=resp_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
        background=response.background,
    )


def _is_suspicious_user_agent(user_agent: str) -> bool:
    user_agent = user_agent.lower()
    return any(keyword in user_agent for keyword in SUSPICIOUS_USER_AGENT_KEYWORDS)


async def block_suspicious_user_agents(request: Request, call_next: Callable) -> Response:
    user_agent = request.headers.get("user-agent")
    if user_agent and _is_suspicious_user_agent(user_agent):
        return JSONResponse(status_code=403, content={"detail": "User-Agent is not allowed"})

    return await call_next(request)
