from datetime import date

from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.user_group import UserGroup
from salonsuite.models.user_status import UserStatus
from salonsuite.models.users import Users


def seed_user_group():
    with Session(engine) as session:
        user_group = [
            UserGroup(name='Proprietario'),
            UserGroup(name='Funcionarios'),
            UserGroup(name='Clientes'),
            UserGroup(name='Fornecedores'),
            UserGroup(name='Gerentes'),
        ]

        session.add_all(user_group)
        session.commit()



if __name__ == '__main__':
    seed_user_group()
