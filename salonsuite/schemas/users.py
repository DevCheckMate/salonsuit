from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class UsersSchemaPublic(BaseModel):
    users_id: int
    image_url: Optional[str]
    email: Optional[str]
    name: str
    group_id: Optional[int]
    group_name: Optional[str]
    cellphone: str
    pin: str
    password: str
    birthdate: Optional[date]
    instagram: Optional[str]
    gender: Optional[str]
    description: Optional[str]
    status_id: int
    status_name: Optional[str]
    created_at: datetime
