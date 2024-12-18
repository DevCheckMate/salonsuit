from fastapi import APIRouter
from .v1.service import router as service_router
from .v1.enterprise import router as enterprise_router

v1_routers = APIRouter(prefix='/salonsuite/v1')

v1_routers.include_router(service_router, prefix='/services', tags=['services'])
v1_routers.include_router(enterprise_router, prefix='/enterprise', tags=['enterprise'])

