from datetime import datetime
from pydantic import BaseModel

class EnterPriseSchemaPublic(BaseModel):
    enterprise_id : int
    name : str
    cnpj : str
    cellphone : str
    email : str
    state : str
    city : str
    cep : str
    status_id : int
    status_name : str
    created_at : datetime
