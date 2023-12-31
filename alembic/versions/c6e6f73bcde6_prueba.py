"""prueba

Revision ID: c6e6f73bcde6
Revises: 2368618b9668
Create Date: 2023-10-03 20:38:58.599950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c6e6f73bcde6'
down_revision: Union[str, None] = '2368618b9668'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_medicine_id', table_name='medicine')
    op.drop_table('medicine')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medicine',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('update_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('drug', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('concentration', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('form', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('gtin', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='medicine_pkey')
    )
    op.create_index('ix_medicine_id', 'medicine', ['id'], unique=False)
    # ### end Alembic commands ###
