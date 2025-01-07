from datetime import date
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import get_session
from salonsuite.models.user_group import UserGroup
from salonsuite.models.user_status import UserStatus
from salonsuite.models.users import Users
from salonsuite.schemas.users import UsersCreateSchema, UsersSchemaPublic

router = APIRouter()


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
    image_url: str = Query(default=None, description='Imagem do Usuário'),
    email: str = Query(default=None, description='Email do usuário'),
    name: str = Query(default=None, description='Nome do Usuário'),
    group_id: int = Query(default=None, description='Aceita 1, 2, 3, 4 e 5'),
    group_name: str = Query(
        default=None, description='Nome do Grupo do usuário'
    ),
    cellphone: str = Query(default=None, description='Telefone do Usuário'),
    pin: str = Query(default=None, description='CPF do Usuário'),
    password: str = Query(default=None, description='Senha do Usuário'),
    birthdate: date = Query(
        default=None, description='Data de Aniversario do Usuário'
    ),
    instagram: str = Query(default=None, description='Instagram do Usuário'),
    gender: str = Query(default=None, description='Gênero do Usuário'),
    description: str = Query(default=None, description='Descrição do Usuário'),
    status_id: int = Query(default=None, description='Aceita 1, 2, 3 e 4'),
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

    if image_url:
        stmt = stmt.where(Users.image_url == image_url)
    if email:
        stmt = stmt.where(Users.email == email)
    if name:
        stmt = stmt.where(Users.name == name)
    if group_id:
        stmt = stmt.where(Users.group_id == group_id)
    if group_name:
        stmt = stmt.where(UserGroup.name == group_name)
    if cellphone:
        stmt = stmt.where(Users.cellphone == cellphone)
    if pin:
        stmt = stmt.where(Users.pin == pin)
    if password:
        stmt = stmt.where(Users.password == password)
    if birthdate:
        stmt = stmt.where(Users.birthdate == birthdate)
    if instagram:
        stmt = stmt.where(Users.instagram == instagram)
    if gender:
        stmt = stmt.where(Users.gender == gender)
    if description:
        stmt = stmt.where(Users.description == description)
    if status_id:
        stmt = stmt.where(Users.status_id == status_id)
    if status_name:
        stmt = stmt.where(UserStatus.name == status_name)

    stmt = stmt.offset(offset).limit(limit).order_by(Users.users_id)

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
    stmt = select(Users).where(Users.users_id == user_id)

    user_db = session.execute(stmt).scalar_one_or_none()

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
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
