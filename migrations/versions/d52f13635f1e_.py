"""empty message

Revision ID: d52f13635f1e
Revises: 3b82c2f70e28
Create Date: 2024-04-04 04:53:39.183045

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd52f13635f1e'
down_revision = '3b82c2f70e28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'document_types', ['type_id'], ['id'])
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('login',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.create_unique_constraint(None, ['login'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('login',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)

    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###