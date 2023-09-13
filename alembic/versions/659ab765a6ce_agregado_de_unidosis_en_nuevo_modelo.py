"""agregado de unidosis en nuevo modelo

Revision ID: 659ab765a6ce
Revises: 5ff7f2faa944
Create Date: 2023-09-12 21:10:19.088848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '659ab765a6ce'
down_revision: Union[str, None] = '5ff7f2faa944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unidosismedicine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('drug', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('concentration', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('form', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('gtin', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('visual_config1', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('visual_config2', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('visual_config3', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('visual_config4', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('adv1', sa.Boolean(), nullable=True),
    sa.Column('adv2', sa.Boolean(), nullable=True),
    sa.Column('adv3', sa.Boolean(), nullable=True),
    sa.Column('adv4', sa.Boolean(), nullable=True),
    sa.Column('adv5', sa.Boolean(), nullable=True),
    sa.Column('tac', sa.Boolean(), nullable=True),
    sa.Column('pregnancy_cat', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_unidosismedicine_id'), 'unidosismedicine', ['id'], unique=False)
    op.drop_index('ix_test_id', table_name='test')
    op.drop_table('test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='test_pkey')
    )
    op.create_index('ix_test_id', 'test', ['id'], unique=False)
    op.drop_index(op.f('ix_unidosismedicine_id'), table_name='unidosismedicine')
    op.drop_table('unidosismedicine')
    # ### end Alembic commands ###
