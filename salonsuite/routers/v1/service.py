from http import HTTPStatus

from fastapi import APIRouter
from sqlalchemy import select

from salonsuite.models.service import Service


router = APIRouter()


@router.get('/{service_id}')
def get_service_by_id(service_id):
    """
        Abaixo é o mesmo que:
        Select * from service where service_id = 1
    """

    stmt = select(Service).where(Service.service_id == service_id)
    return f"Trouxe o servico de id: {service_id}"
