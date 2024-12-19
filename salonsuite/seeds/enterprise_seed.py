from salonsuite.models.enterprise import EnterPrise
from sqlalchemy.orm import Session
from salonsuite.database.db_connection import engine

def seed_enterprises():
    # Adicionar Dados da Tabela Status
    with Session(engine) as session:

        enterprise = [
            EnterPrise(name='SalonSuit', cnpj=65919825000150, cellphone=62991189413,
            email='salonsuit@gmail.com', state='Goiás', city='Goiânia', cep=74890020,
            )
        ]
        session.add_all(enterprise)
        session.commit()

if __name__ == '__main__':
    seed_enterprises()