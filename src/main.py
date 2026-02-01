from fastapi import FastAPI

from src.api.v1.tasks.exception_handlers import task_exception_handler
from src.api.v1.users.exception_handlers import user_exception_handler
from src.api.v1.router import router as v1_router
from src.config import settings
from src.middleware import block_suspicious_user_agents, log_request_response
from src.tasks.exceptions import TaskError
from src.users.exceptions import UserError

app = FastAPI(
    title=settings.app.name,
    debug=settings.app.debug,
)

# Handlers
app.add_exception_handler(TaskError, task_exception_handler)
app.add_exception_handler(UserError, user_exception_handler)

# Routers
app.include_router(v1_router, prefix="/api/v1")

# Middlewares
app.middleware("http")(block_suspicious_user_agents)
app.middleware("http")(log_request_response)
