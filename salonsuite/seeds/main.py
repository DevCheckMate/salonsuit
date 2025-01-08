from sqlalchemy import MetaData, text
from sqlalchemy.orm import Session

from salonsuite.database.db_connection import engine
from salonsuite.seeds.service_category import seed_service_category
from salonsuite.seeds.service_seed import seed_service
from salonsuite.seeds.status import seed_status
from salonsuite.seeds.user_group import seed_user_group
from salonsuite.seeds.user_status import seed_user_status
from salonsuite.seeds.users_seed import seed_user
from salonsuite.seeds.enterprise_seed import seed_enterprise


def clear_all_tables():
    with Session(engine) as session:
        # Carrega todas as tabelas no metadata
        metadata = MetaData()
        metadata.reflect(bind=engine)

        # Desabilitar restrições de chave estrangeira
        session.execute(text('PRAGMA foreign_keys = OFF;'))

        # Apagar dados de cada tabela e resetar autoincrement se necessário
        for table in metadata.sorted_tables:
            session.execute(
                text(f'DELETE FROM {table.name};')
            )  # Limpa os dados

            # Reseta o autoincrement apenas se sqlite_sequence existir
            if (
                'sqlite_sequence'
                in session.execute(
                    text(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';"
                    )
                )
                .scalars()
                .all()
            ):
                session.execute(
                    text(
                        f"DELETE FROM sqlite_sequence WHERE name='{table.name}';"
                    )
                )

        # Reabilitar restrições de chave estrangeira
        session.execute(text('PRAGMA foreign_keys = ON;'))

        # Confirma a transação
        session.commit()


if __name__ == '__main__':
    print('Limpando tabelas')
    clear_all_tables()
    print('Tabelas Truncadas com Sucesso!')
    print('Criação das seeds')
    seed_status()
    seed_user_status()
    seed_user_group()
    seed_user()
    seed_service_category()
    seed_service()
    seed_enterprise()
    print('Concluído com Sucesso!!!')
