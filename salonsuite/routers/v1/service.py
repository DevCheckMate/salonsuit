from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import get_session
from salonsuite.models.service import Service
from salonsuite.models.service_category import ServiceCategory
from salonsuite.models.status import Status
from salonsuite.schemas.services import ServiceSchemaPublic


router = APIRouter()


@router.get('/{service_id}', response_model=ServiceSchemaPublic)
def get_service_by_id(
    service_id: int, session: Session = Depends(get_session)
):
    """
    Abaixo é o mesmo que:
    Select * from service where service_id = 1
    """

    stmt = (
        select(
            Service.service_id,
            Service.name,
            Service.value,
            Service.time,
            Service.service_category_id,
            Service.status_id,
            Service.created_at,
            ServiceCategory.name.label("service_category_name"),
            Status.name.label("status_name")
        )
        .join(ServiceCategory, 
              Service.service_category_id == ServiceCategory.service_category_id)
        .join(Status, Service.status_id == Status.status_id)
        .where(Service.service_id == service_id)    
    )
    
    service_db = session.execute(stmt).mappings().one_or_none()

    if not service_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Service not found'
        )

    '''
    ServiceSchemaPublic(**service_db.__dict__)
    Utiliza dessa forma acima quando o meu contrato(Schema) é exatamente as 
    colunas da minha tabela.

    '''
    data = ServiceSchemaPublic(**dict(service_db))

    return data
