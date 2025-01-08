from pydantic import BaseModel

class EnterPriseSchemaPublic(BaseModel):
    name : str
    cnpj : str
    cellphone : str
    email : str
    state : str
    city : str
    cep : str
    status_id : int
    status_name : str

class EnterPriseCreatSchema(BaseModel):
    name : str
    cnpj : str
    cellphone : str
    email : str
    state : str
    city : str
    cep : str
    status_id : int