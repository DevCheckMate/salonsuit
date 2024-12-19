from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from salonsuite.database.db_connection import get_session
from salonsuite.models.enterprise import EnterPrise


router = APIRouter()

@router.get('/{enterprise_id}')
def get_enterprise_by_id(enterprise_id : int, session : Session = Depends(get_session)):
    stmt = select(EnterPrise).where(EnterPrise.enterprise_id == enterprise_id)
    user_db = session.execute(stmt).scalar_one_or_none()
    return user_db

@router.get('/nome/{var_name}')
def get_enterprise_by_name(enterprise_name : str, session : Session = Depends(get_session)):
    stmt= select(EnterPrise).where(EnterPrise.name == enterprise_name)
    user_db = session.execute(stmt).scalar_one_or_none()
    return user_db