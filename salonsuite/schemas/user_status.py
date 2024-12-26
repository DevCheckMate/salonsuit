from pydantic import BaseModel


class UserStatusSchemaPublic(BaseModel):
    user_group_id: int
    name: str
