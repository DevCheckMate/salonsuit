from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.status import Status


def seed_status():
    with Session(engine) as session:
        status = [Status(name='ATIVO'), Status(name='INATIVO'), Status(name='DELETADO')]
        session.add_all(status)
        session.commit()
    ...


if __name__ == '__main__':
    seed_status()
