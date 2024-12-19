from salonsuite.models.enterprise import EnterPrise
from salonsuite.models.status import Status
from sqlalchemy.orm import Session
from salonsuite.database.db_connection import engine

def seed_services():
    with Session(engine) as session:

        status = [Status(name="ATIVO"), Status(name="INATIVO")]

        enterprise = [
            EnterPrise(name="SalonSuit", cnpj=95375944000150, cellphone=62991189413, email='salonsuit@gmail.com',
                       state='Goiás', city='Goiânia', cep=74890020),
        ]


        session.add_all(status)
        session.commit()
        session.add_all(enterprise)
        session.commit()

    ... 

if __name__ == '__main__':
    seed_services()