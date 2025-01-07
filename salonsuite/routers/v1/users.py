from datetime import datetime
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import get_session
from salonsuite.models.user_group import UserGroup
from salonsuite.models.user_status import UserStatus
from salonsuite.models.users import Users
from salonsuite.schemas.users import UsersCreateSchema, UsersSchemaPublic
from salonsuite.utils.enum import UserStatus as EnumUserStatus

router = APIRouter()


@router.post('', response_model=UsersSchemaPublic)
def create_user(
    body: UsersCreateSchema, session: Session = Depends(get_session)
):
    stmt = select(Users).where(
        or_(
            Users.email == body.email,
            Users.cellphone == body.cellphone,
            Users.pin == body.pin,
            Users.instagram == body.instagram,
        )
    )

    existing_user = session.execute(stmt).scalar_one_or_none()

    if existing_user:
        if existing_user.email == body.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este e-mail.',
            )
        if existing_user.cellphone == body.cellphone:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este Telefone.',
            )
        if existing_user.pin == body.pin:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este Pin(CPF).',
            )
        if existing_user.instagram == body.instagram:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este Instagram.',
            )

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


@router.get('', response_model=List[UsersSchemaPublic])
def list_users(
    page: int = Query(
        default=1, ge=1, description='Número da pagina (começando de 1)'
    ),
    email: str = Query(default=None, description='Email do usuário'),
    name: str = Query(default=None, description='Nome do Usuário'),
    group_name: str = Query(
        default=None, description='Nome do Grupo do usuário'
    ),
    status_name: str = Query(
        default=None, description='Nome do Status do Usuário'
    ),
    session: Session = Depends(get_session),
):
    if page <= 0:
        page = 1

    limit = 3

    offset = (page - 1) * limit

    stmt = (
        select(
            Users.image_url,
            Users.email,
            Users.name,
            Users.group_id,
            UserGroup.name.label('group_name'),
            Users.cellphone,
            Users.pin,
            Users.password,
            Users.birthdate,
            Users.instagram,
            Users.gender,
            Users.description,
            Users.status_id,
            UserStatus.name.label('status_name'),
        )
        .join(UserGroup, Users.group_id == UserGroup.user_group_id)
        .join(UserStatus, Users.status_id == UserStatus.user_status_id)
    )

    if email:
        stmt = stmt.where(Users.email == email)
    if name:
        stmt = stmt.where(Users.name == name)
    if group_name:
        stmt = stmt.where(UserGroup.name == group_name)
    if status_name:
        stmt = stmt.where(UserStatus.name == status_name)

    stmt = (
        stmt.where(Users.status_id != EnumUserStatus.DELETADO.value)
        .offset(offset)
        .limit(limit)
        .order_by(Users.users_id)
    )

    users_db = session.execute(stmt).mappings().all()

    if not users_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    data = list()

    for item in users_db:
        data.append(UsersSchemaPublic(**dict(item)))

    return data


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


@router.put('/{user_id}', response_model=UsersSchemaPublic)
def put_user_by_id(
    user_id: int,
    body: UsersCreateSchema,
    session: Session = Depends(get_session),
):
    stmt = select(Users).where(
        Users.users_id == user_id,
        Users.status_id != EnumUserStatus.DELETADO.value,
    )

    user_db = session.execute(stmt).scalar_one_or_none()

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    stmt = select(Users).where(
        or_(
            Users.email == body.email,
            Users.cellphone == body.cellphone,
            Users.pin == body.pin,
            Users.instagram == body.instagram,
        ),
        Users.users_id != user_id,
    )

    existing_user = session.execute(stmt).scalar_one_or_none()

    if existing_user:
        if existing_user.email == body.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este e-mail.',
            )
        if existing_user.cellphone == body.cellphone:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este Telefone.',
            )
        if existing_user.pin == body.pin:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este Pin(CPF).',
            )
        if existing_user.instagram == body.instagram:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Já existe um usuário com este Instagram.',
            )

    user_db.image_url = body.image_url
    user_db.email = body.email
    user_db.name = body.name
    user_db.group_id = body.group_id
    user_db.cellphone = body.cellphone
    user_db.pin = body.pin
    user_db.password = body.password
    user_db.birthdate = body.birthdate
    user_db.instagram = body.instagram
    user_db.gender = body.gender
    user_db.description = body.description
    user_db.status_id = body.status_id

    session.commit()

    stmt = (
        select(
            Users.image_url,
            Users.email,
            Users.name,
            Users.group_id,
            UserGroup.name.label('group_name'),
            Users.cellphone,
            Users.pin,
            Users.password,
            Users.birthdate,
            Users.instagram,
            Users.gender,
            Users.description,
            Users.status_id,
            UserStatus.name.label('status_name'),
        )
        .join(UserStatus, Users.status_id == UserStatus.user_status_id)
        .join(UserGroup, Users.group_id == UserGroup.user_group_id)
        .where(Users.users_id == user_id)
    )
    user_update_db = session.execute(stmt).mappings().one_or_none()

    data = UsersSchemaPublic(**dict(user_update_db))

    return data


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    stmt = select(Users).where(Users.users_id == user_id)
    user_db = session.execute(stmt).scalar_one_or_none()

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    user_db.deleted_at = datetime.now()
    user_db.status_id = EnumUserStatus.DELETADO.value
    session.commit()
