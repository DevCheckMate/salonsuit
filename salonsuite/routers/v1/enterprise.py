from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from salonsuite.models.status import Status
from salonsuite.utils.enum import Status as EnumStatus

from salonsuite.database.db_connection import get_session
from salonsuite.models.enterprise import EnterPrise
from salonsuite.schemas.enterprise import EnterPriseSchemaPublic, EnterPriseCreatSchema


router = APIRouter()

@router.post('', response_model=EnterPriseSchemaPublic)
def create_enterprise(
    body : EnterPriseCreatSchema, session : Session = Depends(get_session)
    ):
    new_enterprise = EnterPrise(
        name = body.name,
        cnpj = body.cnpj,
        cellphone = body.cellphone,
        email = body.email,
        state = body.state,
        city = body.city,
        cep = body.cep,
        status_id = body.status_id
    )

    current_enterprise = session.query(EnterPrise).all()
    for enterprise in current_enterprise:
        if enterprise.cellphone == body.cellphone:
            raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='cellphone already exist'
        )
        if enterprise.cnpj == body.cnpj:
            raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='cnpj already exist'
        )
        if enterprise.email == body.email:
            raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email already exist'
        )

    session.add(new_enterprise)
    session.commit()
    session.refresh(new_enterprise)

    stmt = (
        select(
            EnterPrise.name,
            EnterPrise.cnpj,
            EnterPrise.cellphone,
            EnterPrise.email,
            EnterPrise.state,
            EnterPrise.city,
            EnterPrise.cep,
            EnterPrise.status_id,
            Status.name.label("status_name")
        ).join(
            Status, EnterPrise.status_id == Status.status_id
            ).where(
            EnterPrise.enterprise_id == new_enterprise.enterprise_id
        )
    )
    new_enterprise_db = session.execute(stmt).mappings().one_or_none()

    new_enterprise_data = EnterPriseSchemaPublic(**dict(new_enterprise_db))

    return new_enterprise_data

@router.get('/{enterprise_id}', response_model=EnterPriseSchemaPublic)
def get_enterprise_by_id(
    enterprise_id: int, session: Session = Depends(get_session)
):
    
    stmt = select(
        EnterPrise.enterprise_id,
        EnterPrise.name,
        EnterPrise.cnpj,
        EnterPrise.cellphone,
        EnterPrise.email,
        EnterPrise.state,
        EnterPrise.city,
        EnterPrise.cep,
        EnterPrise.status_id,
        Status.name.label("status_name")
    ).join(
        Status, EnterPrise.status_id == Status.status_id
        ).where(
        EnterPrise.enterprise_id == enterprise_id,
        EnterPrise.status_id != EnumStatus.DELETADO.value
        )
    
    enterprise_db = session.execute(stmt).mappings().one_or_none()

    if not enterprise_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='enterprise not found'
        )
    data = EnterPriseSchemaPublic(**dict(enterprise_db))

    return data

@router.put('/{enterprise_id}', response_model=EnterPriseSchemaPublic)
def put_enterprise_by_id(
    enterprise_id: int, body: EnterPriseCreatSchema, 
    session: Session = Depends(get_session)
):
    stmt = select(EnterPrise).where(EnterPrise.enterprise_id == enterprise_id,
                                    EnterPrise.status_id != EnumStatus.DELETADO.value
                                    )
    enterprise_db = session.execute(stmt).scalar_one_or_none()

    if not enterprise_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Enterprise Not Found'
        )

    enterprise_db.name = body.name
    enterprise_db.cnpj = body.cnpj
    enterprise_db.cellphone = body.cellphone
    enterprise_db.email = body.email
    enterprise_db.state = body.state
    enterprise_db.city = body.city
    enterprise_db.cep = body.cep
    enterprise_db.status_id = body.status_id

    session.commit()

    stmt = (
        select(
            EnterPrise.enterprise_id,
            EnterPrise.name,
            EnterPrise.cnpj,
            EnterPrise.cellphone,
            EnterPrise.email,
            EnterPrise.state,
            EnterPrise.city,
            EnterPrise.cep,
            EnterPrise.status_id,
            Status.name.label("status_name")
        ).join(
            Status, EnterPrise.status_id == Status.status_id
        ).where(
            EnterPrise.enterprise_id == enterprise_id,
            EnterPrise.status_id != EnumStatus.DELETADO.value
        )
    )

    enterprise_update_db = session.execute(stmt).mappings().one_or_none()

    data = EnterPriseSchemaPublic(**dict(enterprise_update_db))

    return data