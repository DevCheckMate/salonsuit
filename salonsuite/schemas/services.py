from pydantic import BaseModel


class ServiceSchemaPublic(BaseModel):
    service: str
    price: int
    service_time: int
    status: str
    category: str


class ServiceCreateSchema(BaseModel):
    service: str
    price: int
    service_time: int
    status: int
    category: int
