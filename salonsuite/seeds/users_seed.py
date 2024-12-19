from datetime import date

from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.user_group import UserGroup
from salonsuite.models.user_status import UserStatus
from salonsuite.models.users import Users


def seed_users():
    with Session(engine) as session:
        user_status = [UserStatus(name='ATIVO'), UserStatus(name='INATIVO')]

        user_group = [
            UserGroup(name='Proprietario'),
            UserGroup(name='Funcionarios'),
            UserGroup(name='Clientes'),
            UserGroup(name='Fornecedores'),
            UserGroup(name='Gerentes'),
        ]

        users = [
            Users(
                image_url='https://example.com/image1.jpg',
                email='fillipe@example.com',
                name='Fillipe',
                group_id=1,
                cellphone='91536058',
                pin='03178494170',
                password='1234',
                birthdate=date(1995, 7, 6),
                instagram='@fillipeberssot',
                gender='Male',
                description='Primerio usuario criado',
            ),
            Users(
                image_url=None,
                email=None,
                name='Thiago',
                group_id=2,
                cellphone='952521452',
                pin='03178441520',
                password='1234',
                birthdate=None,
                instagram=None,
                gender='Male',
                description='Segundo usuario criado',
            ),
            Users(
                image_url='https://example.com/image2.jpg',
                email='alberdan@example.com',
                name='Alberdan',
                group_id=3,
                cellphone='991587482',
                pin='12541874512',
                password='1234',
                birthdate=None,
                instagram=None,
                gender='Male',
                description='Terceiro usuario criado',
            ),
        ]

        session.add_all(user_status)
        session.commit()
        session.add_all(user_group)
        session.commit()
        session.add_all(users)
        session.commit()


if __name__ == '__main__':
    seed_users()
