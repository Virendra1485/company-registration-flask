"""empty message

Revision ID: ac0f42572134
Revises: 
Create Date: 2024-04-04 22:11:44.500762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac0f42572134'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accreditations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accreditation_name', sa.String(length=220), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=220), nullable=True),
    sa.Column('email', sa.String(length=220), nullable=True),
    sa.Column('password_hash', sa.String(length=220), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('manufactured_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=220), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offered_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_name', sa.String(length=220), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cmo', sa.String(length=220), nullable=False),
    sa.Column('manufacturing_site', sa.String(length=220), nullable=False),
    sa.Column('address', sa.String(length=220), nullable=False),
    sa.Column('country', sa.Enum('INDIA', 'RUSSIA', name='countrychoice'), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_accreditation',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('accreditations_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['accreditations_id'], ['accreditations.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['company_details.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'accreditations_id')
    )
    op.create_table('company_manufacture_product',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('manufactured_products_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company_details.id'], ),
    sa.ForeignKeyConstraint(['manufactured_products_id'], ['manufactured_products.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'manufactured_products_id')
    )
    op.create_table('company_offered_services',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('offered_service_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company_details.id'], ),
    sa.ForeignKeyConstraint(['offered_service_id'], ['offered_services.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'offered_service_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('company_offered_services')
    op.drop_table('company_manufacture_product')
    op.drop_table('company_accreditation')
    op.drop_table('company_details')
    op.drop_table('offered_services')
    op.drop_table('manufactured_products')
    op.drop_table('companies')
    op.drop_table('accreditations')
    # ### end Alembic commands ###
