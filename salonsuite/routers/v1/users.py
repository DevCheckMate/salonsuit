from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import get_session
from salonsuite.models.user_group import UserGroup
from salonsuite.models.user_status import UserStatus
from salonsuite.models.users import Users
from salonsuite.schemas.users import UsersCreateSchema, UsersSchemaPublic

router = APIRouter()


@router.get('/{user_id}', response_model=UsersSchemaPublic)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    stmt = (
        select(
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
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    data = UsersSchemaPublic(**dict(user_db))

    return data


@router.post('', response_model=UsersSchemaPublic)
def create_user(
    body: UsersCreateSchema, session: Session = Depends(get_session)
):
    new_user = Users(
        image_url=body.image_url,
        email=body.email,
        name=body.name,
        group_id=body.group_id,
        cellphone=body.cellphone,
        pin=body.pin,
        password=body.password,
        birthdate=body.birthdate,
        instagram=body.instagram,
        gender=body.gender,
        description=body.description,
        status_id=body.status_id,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

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
            UserGroup.name.label('group_name'),
            UserStatus.name.label('status_name'),
        )
        .join(UserGroup, Users.group_id == UserGroup.user_group_id)
        .join(UserStatus, Users.status_id == UserStatus.user_status_id)
        .where(Users.users_id == new_user.users_id)
    )

    new_user_db = session.execute(stmt).mappings().one_or_none()
    new_user_data = UsersSchemaPublic(**dict(new_user_db))

    return new_user_data
