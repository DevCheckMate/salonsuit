"""criacao_tabela_users

Revision ID: cd18239f3026
Revises: 1be3a9604875
Create Date: 2024-12-16 14:46:35.053200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd18239f3026'
down_revision: Union[str, None] = '1be3a9604875'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('users_email', sa.String(length=255), nullable=True),
    sa.Column('users_name', sa.String(length=100), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('users_cellphone', sa.String(length=11), nullable=False),
    sa.Column('users_pin', sa.String(length=11), nullable=False),
    sa.Column('users_password', sa.String(length=255), nullable=False),
    sa.Column('users_birthdate', sa.Date(), nullable=True),
    sa.Column('users_instagram', sa.String(length=100), nullable=True),
    sa.Column('users_gender', sa.String(length=6), nullable=True),
    sa.Column('users_description', sa.String(length=255), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('users_image_url', sa.String(length=255), nullable=True),
    sa.Column('users_created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('users_update_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('users_deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['status_id'], ['status.status_id'], ),
    sa.PrimaryKeyConstraint('users_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
