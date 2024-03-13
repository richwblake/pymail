"""adds foreign keys to messages and messagefields

Revision ID: e20142faf024
Revises: ad7520241176
Create Date: 2024-03-13 10:12:51.041327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e20142faf024'
down_revision = 'ad7520241176'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message_fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_message_fields_message_id_messages'), 'messages', ['message_id'], ['id'])

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('receiver_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_messages_receiver_id_receivers'), 'receivers', ['receiver_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_messages_receiver_id_receivers'), type_='foreignkey')
        batch_op.drop_column('receiver_id')

    with op.batch_alter_table('message_fields', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_message_fields_message_id_messages'), type_='foreignkey')
        batch_op.drop_column('message_id')

    # ### end Alembic commands ###
