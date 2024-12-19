from fastapi import APIRouter, Depends
from pytest import Session
from sqlalchemy import select

from salonsuite.database.db_connection import get_session
from salonsuite.models.users import Users

router = APIRouter()


@router.get('/{user_id}')
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    stmt = select(Users).where(Users.users_id == user_id)
    user_db = session.execute(stmt).scalar_one_or_none()
    return user_db


@router.get('/nome/{var_name}')
def get_user_by_id(var_name: str, session: Session = Depends(get_session)):
    stmt = select(Users).where(Users.name == var_name)
    user_db = session.execute(stmt).scalar_one_or_none()
    return user_db
