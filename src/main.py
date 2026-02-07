from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.tasks.exception_handlers import task_exception_handler
from src.api.v1.users.exception_handlers import user_exception_handler
from src.api.v1.router import router as v1_router
from src.config import settings
from src.middleware import block_suspicious_user_agents, log_request_response
from src.tasks.cache import create_task_list_cache
from src.tasks.exceptions import TaskError
from src.users.exceptions import UserError


@asynccontextmanager
async def lifespan(app: FastAPI):
    task_list_cache = create_task_list_cache()
    app.state.task_list_cache = task_list_cache
    yield
    await task_list_cache.close()


app = FastAPI(
    title=settings.app.name,
    debug=settings.app.debug,
    lifespan=lifespan,
)

# Handlers
app.add_exception_handler(TaskError, task_exception_handler)
app.add_exception_handler(UserError, user_exception_handler)

# Routers
app.include_router(v1_router, prefix="/api/v1")

# Middlewares
app.middleware("http")(block_suspicious_user_agents)
app.middleware("http")(log_request_response)
