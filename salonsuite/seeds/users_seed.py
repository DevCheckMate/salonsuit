from datetime import date

from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.user_group import UserGroup
from salonsuite.models.user_status import UserStatus
from salonsuite.models.users import Users


def seed_user():
    with Session(engine) as session:
        users = [
            Users(
                image_url='https://example.com/image1.jpg',
                email='fillipe@example.com',
                name='Fillipe',
                group_id=1,
                cellphone='91536058',
                pin='03178494170',
                password='123',
                birthdate=date(1995, 7, 6),
                instagram='@fillipeberssot',
                gender='Male',
                description='Primerio usuario criado',
            ),
            Users(
                image_url=None,
                email='thiago@example.com',
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
                password='12345',
                birthdate=None,
                instagram=None,
                gender='Male',
                description='Terceiro usuario criado',
            ),
        ]

        session.add_all(users)
        session.commit()

if __name__ == '__main__':
    seed_user()
