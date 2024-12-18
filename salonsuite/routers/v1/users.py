from fastapi import APIRouter, Depends
from pytest import Session
from sqlalchemy import select

from salonsuite.database.db_connection import get_session
from salonsuite.models.users import Users


router = APIRouter()

@router.get('/{user_id}')
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):

    stmt = select(Users).where(Users.users_id == user_id)
    return {f'Usuario de id: {user_id} encontrado'}
