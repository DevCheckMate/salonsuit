from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import get_session
from salonsuite.models.service import Service
from salonsuite.models.service_category import ServiceCategory
from salonsuite.models.status import Status
from salonsuite.schemas.services import ServiceSchemaPublic, ServiceCreateSchema


router = APIRouter()


@router.get('/{service_id}', response_model=ServiceSchemaPublic)
def get_service_by_id(service_id: int, session: Session = Depends(get_session)):
    stmt = (
        select(
            Service.name.label('service'), 
            Service.value.label('price'), 
            Service.time.label('service_time'), 
            Status.name.label('status'), 
            ServiceCategory.name.label('category')
        )
        .join(Status, Status.status_id == Service.status_id)
        .join(ServiceCategory, ServiceCategory.service_category_id == Service.service_category_id)
        .where(Service.service_id == service_id)
    )
    service_db= session.execute(stmt).mappings().one_or_none()

    if not service_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Service Not Found'
        )

    data = ServiceSchemaPublic(**dict(service_db))

    return data

@router.post('', response_model=ServiceSchemaPublic)
def create_service(body: ServiceCreateSchema, session: Session = Depends(get_session)):
    ...
    new_service = Service(
        name=body.service,
        value=body.price,
        time=body.service_time,
        service_category_id=body.category,
        status_id=body.status
    )

    session.add(new_service)
    session.commit()
    session.refresh(new_service)


    stmt = (
        select(
            Service.name.label('service'), 
            Service.value.label('price'), 
            Service.time.label('service_time'), 
            Status.name.label('status'), 
            ServiceCategory.name.label('category')
        )
        .join(Status, Status.status_id == Service.status_id)
        .join(ServiceCategory, ServiceCategory.service_category_id == Service.service_category_id)
        .where(Service.service_id == new_service.service_id)
    )

    new_service_db= session.execute(stmt).mappings().one_or_none()
    new_service_data = ServiceSchemaPublic(**dict(new_service_db))

    return new_service_data