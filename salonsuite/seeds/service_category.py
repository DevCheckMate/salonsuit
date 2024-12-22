from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.service_category import ServiceCategory


def seed_service_category():
    with Session(engine) as session:
        services_category = [
            ServiceCategory(name='Cortes Masculinos'),
            ServiceCategory(name='Barba'),
            ServiceCategory(name='Cortes Femininos'),
        ]
        session.add_all(services_category)
        session.commit()

    ...


if __name__ == '__main__':
    seed_service_category()
