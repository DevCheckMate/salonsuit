from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from sqlalchemy import select

from salonsuite.database.db_connection import get_session
from salonsuite.models.user_group import UserGroup
from salonsuite.models.user_status import UserStatus
from salonsuite.models.users import Users
from salonsuite.schemas.users import UsersSchemaPublic

router = APIRouter()


@router.get('/{user_id}', response_model=UsersSchemaPublic)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    stmt = (
        select(
            Users.users_id,
            Users.image_url,
            Users.email,
            Users.name,
            Users.group_id,
            Users.cellphone,
            Users.pin,
            Users.password,
            Users.birthdate,
            Users.instagram,
            Users.gender,
            Users.description,
            Users.status_id,
            Users.created_at,
            UserGroup.name.label('group_name'),
            UserStatus.name.label('status_name'),
        )
        .join(UserGroup, Users.group_id == UserGroup.user_group_id)
        .join(UserStatus, Users.status_id == UserStatus.user_status_id)
        .where(Users.users_id == user_id)
    )

    user_db = session.execute(stmt).mappings().one_or_none()

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    data = UsersSchemaPublic(**dict(user_db))

    return data
