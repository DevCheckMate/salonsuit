from fastapi import APIRouter

from .v1.service import router as service_router
from .v1.users import router as users_router

v1_routers = APIRouter(prefix='/salonsuite/v1')

v1_routers.include_router(
    service_router, prefix='/services', tags=['services']
)
v1_routers.include_router(users_router, prefix='/users', tags=['users'])
