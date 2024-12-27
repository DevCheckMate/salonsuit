from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from salonsuite.models.status import Status

from salonsuite.database.db_connection import get_session
from salonsuite.models.enterprise import EnterPrise
from salonsuite.schemas.enterprise import EnterPriseSchemaPublic

router = APIRouter()


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
        Status.name.label("status_name"),
        EnterPrise.created_at,
    ).join(
        Status, EnterPrise.status_id == Status.status_id
        ).where(
        EnterPrise.enterprise_id == enterprise_id
        )
    
    enterprise_db = session.execute(stmt).mappings().one_or_none()

    if not enterprise_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='enterprise not found'
        )
    data = EnterPriseSchemaPublic(**dict(enterprise_db))

    return data

