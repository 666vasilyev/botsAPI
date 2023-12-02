"""add active folder to Bot

Revision ID: 7a7e68207411
Revises: 2ee86904292b
Create Date: 2023-09-29 23:14:28.932569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a7e68207411'
down_revision = '2ee86904292b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Bots', sa.Column('active', sa.Boolean(), server_default='True', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Bots', 'active')
    # ### end Alembic commands ###