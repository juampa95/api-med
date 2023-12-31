"""prueba

Revision ID: ee6e7809f3a0
Revises: 5815e5305a85
Create Date: 2023-10-03 20:40:11.133328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ee6e7809f3a0'
down_revision: Union[str, None] = '5815e5305a85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doctor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.Column('personal_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('lastname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_doctor_id'), 'doctor', ['id'], unique=False)
    op.create_table('medicine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('drug', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('concentration', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('form', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('gtin', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medicine_id'), 'medicine', ['id'], unique=False)
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.Column('personal_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('lastname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patient_id'), 'patient', ['id'], unique=False)
    op.create_table('prescription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prescription_id'), 'prescription', ['id'], unique=False)
    op.create_table('prescriptiondetails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.Column('prescription_id', sa.Integer(), nullable=False),
    sa.Column('medicine_id', sa.Integer(), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['medicine_id'], ['medicine.id'], ),
    sa.ForeignKeyConstraint(['prescription_id'], ['prescription.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prescriptiondetails_id'), 'prescriptiondetails', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_prescriptiondetails_id'), table_name='prescriptiondetails')
    op.drop_table('prescriptiondetails')
    op.drop_index(op.f('ix_prescription_id'), table_name='prescription')
    op.drop_table('prescription')
    op.drop_index(op.f('ix_patient_id'), table_name='patient')
    op.drop_table('patient')
    op.drop_index(op.f('ix_medicine_id'), table_name='medicine')
    op.drop_table('medicine')
    op.drop_index(op.f('ix_doctor_id'), table_name='doctor')
    op.drop_table('doctor')
    # ### end Alembic commands ###
