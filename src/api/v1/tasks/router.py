from fastapi import APIRouter

# Импортируем эндпоинты из модулей
from src.api.v1.tasks.get_list import endpoint as get_list
from src.api.v1.tasks.get_by_id import endpoint as get_by_id
from src.api.v1.tasks.create import endpoint as create
from src.api.v1.tasks.update import endpoint as update
from src.api.v1.tasks.delete import endpoint as delete_endpoint
from src.api.v1.tasks.stats_total import endpoint as stats_total
from src.api.v1.tasks.stats_by_day import endpoint as stats_by_day
from src.api.v1.tasks.active_users import endpoint as active_users


tasks_router = APIRouter()


tasks_router.add_api_route(
    **get_list.ENDPOINT_CONFIG,
    endpoint=get_list.get_all_tasks,
)

tasks_router.add_api_route(
    **get_by_id.ENDPOINT_CONFIG,
    endpoint=get_by_id.get_task_by_id,
)

tasks_router.add_api_route(
    **create.ENDPOINT_CONFIG,
    endpoint=create.create_task,
)

tasks_router.add_api_route(
    **update.ENDPOINT_CONFIG,
    endpoint=update.update_task,
)

tasks_router.add_api_route(
    **delete_endpoint.ENDPOINT_CONFIG,
    endpoint=delete_endpoint.delete_task,
)

tasks_router.add_api_route(
    **stats_total.ENDPOINT_CONFIG,
    endpoint=stats_total.get_task_stats,
)

tasks_router.add_api_route(
    **stats_by_day.ENDPOINT_CONFIG,
    endpoint=stats_by_day.get_tasks_by_day,
)

tasks_router.add_api_route(
    **active_users.ENDPOINT_CONFIG,
    endpoint=active_users.get_active_users,
)
