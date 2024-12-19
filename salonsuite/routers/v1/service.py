from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import get_session
from salonsuite.models.service import Service

router = APIRouter()


@router.get('/{service_id}')
def get_service_by_id(
    service_id: int, session: Session = Depends(get_session)
):
    """
    Abaixo é o mesmo que:
    Select * from service where service_id = 1
    """

    stmt = select(Service).where(Service.service_id == service_id)
    user_db = session.execute(stmt).scalar_one_or_none()
    return user_db


@router.get('/nome/{var_name}')
def get_service_by_id(var_name: str, session: Session = Depends(get_session)):
    """
    Abaixo é o mesmo que:
    Select * from service where name = "Long Bob"
    """

    stmt = select(Service).where(Service.name == var_name)
    user_db = session.execute(stmt).scalar_one_or_none()
    return user_db
