from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.models.enterprise import EnterPrise


def seed_enterprise():
    with Session(engine) as session:
        enterprise = [
            EnterPrise(
                name='Rei da Navalha',
                cnpj='12345678000100',
                cellphone='62991112233',
                email='reidanavalha@gmail.com',
                state='Goiás',
                city='Goiânia',
                cep='74810000',
            ),
            EnterPrise(
                name='Gr Cortes',
                cnpj='23456789000111',
                cellphone='61992233444',
                email='grcortes@gmail.com',
                state='Distrito Federal',
                city='Brasília',
                cep='70040900',
            ),
            EnterPrise(
                name='Bexior',
                cnpj='34567891000122',
                cellphone='11993344555',
                email='bexior@gmail.com',
                state='São Paulo',
                city='São Paulo',
                cep='01010901',
            ),
            EnterPrise(
                name='Los Hermanos Barbearia',
                cnpj='45678912000133',
                cellphone='31994455666',
                email='hermanosbarbearia@gmail.com',
                state='Minas Gerais',
                city='Belo Horizonte',
                cep='30120010',
            ),
            EnterPrise(
                name='Edom Barbearia',
                cnpj='56789123000144',
                cellphone='41995566777',
                email='edombarbearia@gmail.com',
                state='Paraná',
                city='Curitiba',
                cep='80020020',
            ),
            EnterPrise(
                name='American Barbershop',
                cnpj='67891234000155',
                cellphone='51996677888',
                email='americanbarbershop@gmail.com',
                state='Rio Grande do Sul',
                city='Porto Alegre',
                cep='90030030',
            ),
            EnterPrise(
                name='Barber House',
                cnpj='78912345000166',
                cellphone='71997788999',
                email='barberhouse@gmail.com',
                state='Bahia',
                city='Salvador',
                cep='40040040',
            ),
            EnterPrise(
                name='Barbearia hora',
                cnpj='89123456000177',
                cellphone='81998899000',
                email='barbeariahora@gmail.com',
                state='Pernambuco',
                city='Recife',
                cep='50050050',
            ),
            EnterPrise(
                name='Oficina do Corte',
                cnpj='91234567000188',
                cellphone='65999900111',
                email='oficinadocorte@gmail.com',
                state='Mato Grosso',
                city='Cuiabá',
                cep='78060060',
            ),
            EnterPrise(
                name='Elite Barber Shop',
                cnpj='12345678000199',
                cellphone='81990111222',
                email='elitebarbershop@gmail.com',
                state='Pernambuco',
                city='Olinda',
                cep='53070070',
            ),
        ]
        session.add_all(enterprise)
        session.commit()

if __name__ == '__main__':
    seed_enterprise()