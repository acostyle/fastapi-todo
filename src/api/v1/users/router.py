from fastapi import APIRouter

from src.api.v1.users.get_by_id import endpoint as get_by_id
from src.api.v1.users.login import endpoint as login
from src.api.v1.users.register import endpoint as register


users_router = APIRouter()


users_router.add_api_route(
    **register.ENDPOINT_CONFIG,
    endpoint=register.register_user,
)

users_router.add_api_route(
    **login.ENDPOINT_CONFIG,
    endpoint=login.login_user,
)

users_router.add_api_route(
    **get_by_id.ENDPOINT_CONFIG,
    endpoint=get_by_id.get_user_by_id,
)
