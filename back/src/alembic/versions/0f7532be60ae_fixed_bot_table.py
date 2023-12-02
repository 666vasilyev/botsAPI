"""fixed Bot table

Revision ID: 0f7532be60ae
Revises: cb73fc9ef892
Create Date: 2023-09-28 23:17:18.496193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f7532be60ae'
down_revision = 'cb73fc9ef892'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Bots_alias_key', 'Bots', type_='unique')
    op.drop_constraint('Bots_description_key', 'Bots', type_='unique')
    op.drop_constraint('Bots_name_key', 'Bots', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('Bots_name_key', 'Bots', ['name'])
    op.create_unique_constraint('Bots_description_key', 'Bots', ['description'])
    op.create_unique_constraint('Bots_alias_key', 'Bots', ['alias'])
    # ### end Alembic commands ###