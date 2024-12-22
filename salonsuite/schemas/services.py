from datetime import datetime

from pydantic import BaseModel


class ServiceSchemaPublic(BaseModel):
    service_id: int
    name: str
    value: int
    time: int
    service_category_id: int
    service_category_name: str
    status_id: int
    status_name: str
    created_at: datetime
