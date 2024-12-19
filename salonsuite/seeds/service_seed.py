from salonsuite.models.service import Service
from salonsuite.models.service_category import ServiceCategory
from salonsuite.models.status import Status
from sqlalchemy.orm import Session
from salonsuite.database.db_connection import engine

def seed_services():
    # Adicionar Dados da Tabela Status
    with Session(engine) as session:

        status = [Status(name="ATIVO"), Status(name="INATIVO")]

        services_category = [
            ServiceCategory(name="Cortes Masculinos"), 
            ServiceCategory(name="Barba"),
            ServiceCategory(name="Cortes Femininos")
        ]

        services = [
            Service(name="Taper", value=100, time=30, service_category_id=1),
            Service(name="Low Fade", value=110, time=40, service_category_id=1),
            Service(name="Mid Fade", value=120, time=50, service_category_id=1),
            Service(name="High Fade", value=130, time=60, service_category_id=1),
            Service(name="The Zappa", value=100, time=30, service_category_id=2),
            Service(name="Sparrow", value=100, time=30, service_category_id=2),
            Service(name="Klingon", value=100, time=30, service_category_id=2),
            Service(name="Duli", value=100, time=30, service_category_id=2),
            Service(name="Pixie", value=250, time=30, service_category_id=3),
            Service(name="Long Bob", value=300, time=30, service_category_id=3),
            Service(name="Short Bob", value=250, time=30, service_category_id=3),
            Service(name="Chanel", value=350, time=30, service_category_id=3)
        
        ]


        session.add_all(status)
        session.commit()
        session.add_all(services_category)
        session.commit()
        session.add_all(services)
        session.commit()

    ... 

if __name__ == '__main__':
    seed_services()