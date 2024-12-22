from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.service import Service


def seed_service():
    with Session(engine) as session:
        services = [
            Service(name='Taper', value=100, time=30, service_category_id=1),
            Service(
                name='Low Fade', value=110, time=40, service_category_id=1
            ),
            Service(
                name='Mid Fade', value=120, time=50, service_category_id=1
            ),
            Service(
                name='High Fade', value=130, time=60, service_category_id=1
            ),
            Service(
                name='The Zappa', value=100, time=30, service_category_id=2
            ),
            Service(name='Sparrow', value=100, time=30, service_category_id=2),
            Service(name='Klingon', value=100, time=30, service_category_id=2),
            Service(name='Duli', value=100, time=30, service_category_id=2),
            Service(name='Pixie', value=250, time=30, service_category_id=3),
            Service(
                name='Long Bob', value=300, time=30, service_category_id=3
            ),
            Service(
                name='Short Bob', value=250, time=30, service_category_id=3
            ),
            Service(name='Chanel', value=350, time=30, service_category_id=3),
        ]

        session.add_all(services)
        session.commit()

    ...


if __name__ == '__main__':
    seed_service()
