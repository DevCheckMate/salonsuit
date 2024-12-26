from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.user_status import UserStatus


def seed_user_status():
    with Session(engine) as session:
        user_status = [
            UserStatus(name='ATIVO'),
            UserStatus(name='INATIVO'),
            UserStatus(name='DEMITIDO'),
            UserStatus(name='FÉRIAS'),
        ]

        session.add_all(user_status)
        session.commit()


if __name__ == '__main__':
    seed_user_status()
