from pydantic import BaseModel


class StatusSchemaPublic(BaseModel):
    status_id: int
    name: str
