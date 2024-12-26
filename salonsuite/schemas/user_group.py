from pydantic import BaseModel


class UserGroupSchemaPublic(BaseModel):
    user_group_id: int
    name: str
