from datetime import datetime
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import get_session
from salonsuite.models.service import Service
from salonsuite.models.service_category import ServiceCategory
from salonsuite.models.status import Status
from salonsuite.schemas.services import (
    ServiceCreateSchema,
    ServiceSchemaPublic,
)

from salonsuite.utils.enum import Status as EnumStatus

router = APIRouter()


@router.post('', response_model=ServiceSchemaPublic)
def create_service(
    body: ServiceCreateSchema, session: Session = Depends(get_session)
):
    ...
    new_service = Service(
        name=body.service,
        value=body.price,
        time=body.service_time,
        service_category_id=body.category,
        status_id=body.status,
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
            ServiceCategory.name.label('category'),
        )
        .join(Status, Status.status_id == Service.status_id)
        .join(
            ServiceCategory,
            ServiceCategory.service_category_id == Service.service_category_id,
        )
        .where(Service.service_id == new_service.service_id)
    )

    new_service_db = session.execute(stmt).mappings().one_or_none()
    new_service_data = ServiceSchemaPublic(**dict(new_service_db))

    return new_service_data


@router.get('', response_model=List[ServiceSchemaPublic])
def list_services(
    page: int = Query(default=1, ge=1, description="Número da página (começando de 1)"), 
    price_min: int = Query(default=None, ge=1, description="Preço mínimo do serviço"),
    price_max: int = Query(default=None, ge=1, description="Preço máximo do serviço"),
    service: str = Query(default=None, description="Serviço"),
    status: int = Query(default=1, description="Aceita 1 e 2"),
    category: int = Query(default=None, description="Categoria do Serviço"),
    session: Session = Depends(get_session)
):
    
    if page <= 0:
        page = 1
    
    limit = 3

    offset = (page - 1) * limit

    stmt = (
        select(
            Service.name.label('service'),
            Service.value.label('price'),
            Service.time.label('service_time'),
            Status.name.label('status'),
            ServiceCategory.name.label('category'),
        )
        .join(Status, Status.status_id == Service.status_id)
        .join(
            ServiceCategory,
            ServiceCategory.service_category_id == Service.service_category_id,
        )
    )

    if price_min:
        stmt = stmt.where(Service.value >= price_min)
    if price_max: 
        stmt = stmt.where(Service.value <= price_max)
    if service:
        stmt = stmt.where(Service.name.ilike(f"%{service}%"))
    if status:
        stmt = stmt.where(Service.status_id == status)
    if category:
        stmt = stmt.where(Service.service_category_id == category)
    
    stmt = (
        stmt.where(Service.status_id != EnumStatus.DELETADO.value)
        .offset(offset)
        .limit(limit)
        .order_by(Service.service_id))

    services_db = session.execute(stmt).mappings().all()

    if not services_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Service Not Found'
        )
    
    data = list()

    for item in services_db:
        data.append(ServiceSchemaPublic(**dict(item)))

    return data



@router.get('/{service_id}', response_model=ServiceSchemaPublic)
def get_service_by_id(
    service_id: int, session: Session = Depends(get_session)
):
    stmt = (
        select(
            Service.name.label('service'),
            Service.value.label('price'),
            Service.time.label('service_time'),
            Status.name.label('status'),
            ServiceCategory.name.label('category'),
        )
        .join(Status, Status.status_id == Service.status_id)
        .join(
            ServiceCategory,
            ServiceCategory.service_category_id == Service.service_category_id,
        )
        .where(Service.service_id == service_id, 
               Service.status_id != EnumStatus.DELETADO.value)
    )
    service_db = session.execute(stmt).mappings().one_or_none()

    if not service_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Service Not Found'
        )

    data = ServiceSchemaPublic(**dict(service_db))

    return data

@router.put('/{service_id}', response_model=ServiceSchemaPublic)
def put_service_by_id(
    service_id: int, body: ServiceCreateSchema, session: Session = Depends(get_session)
):
    stmt = select(Service).where(Service.service_id == service_id, 
                                 Service.status_id != EnumStatus.DELETADO.value)
    
    service_db = session.execute(stmt).scalar_one_or_none()

    if not service_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Service Not Found'
        )
    
    service_db.name = body.service
    service_db.value = body.price
    service_db.time = body.service_time
    service_db.status_id = body.status
    service_db.service_category_id = body.category

    session.commit()

    stmt = (
        select(
            Service.name.label('service'),
            Service.value.label('price'),
            Service.time.label('service_time'),
            Status.name.label('status'),
            ServiceCategory.name.label('category'),
        )
        .join(Status, Status.status_id == Service.status_id)
        .join(
            ServiceCategory,
            ServiceCategory.service_category_id == Service.service_category_id,
        )
        .where(Service.service_id == service_id)
    )
    service_update_db = session.execute(stmt).mappings().one_or_none()

    data = ServiceSchemaPublic(**dict(service_update_db))

    return data


@router.delete('/{service_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_service_by_id(
    service_id: int, session: Session = Depends(get_session)
):
    stmt = select(Service).where(Service.service_id == service_id)
    service_db = session.execute(stmt).scalar_one_or_none()

    if not service_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Service Not Found'
        )
    
    service_db.deleted_at = datetime.now()
    service_db.status_id = EnumStatus.DELETADO.value
    session.commit()