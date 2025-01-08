"""criacao_enterprise

Revision ID: a1c4e3404a32
Revises: 203c6ebd3116
Create Date: 2024-12-27 10:44:15.040551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c4e3404a32'
down_revision: Union[str, None] = '203c6ebd3116'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enterprise',
    sa.Column('enterprise_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('cnpj', sa.String(length=14), nullable=False),
    sa.Column('cellphone', sa.String(length=11), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('cep', sa.String(length=8), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('deleted_at', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['status_id'], ['status.status_id'], ),
    sa.PrimaryKeyConstraint('enterprise_id'),
    sa.UniqueConstraint('cellphone'),
    sa.UniqueConstraint('cnpj'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('enterprise')
    # ### end Alembic commands ###