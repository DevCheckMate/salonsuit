from pydantic import BaseModel


class ServiceCategorySchemaPublic(BaseModel):
    service_category_id: int
    name: str
