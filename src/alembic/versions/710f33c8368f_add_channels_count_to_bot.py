"""add 'channels_count' to Bot

Revision ID: 710f33c8368f
Revises: 90421e74de2b
Create Date: 2023-05-12 12:11:58.568305

"""
<<<<<<< HEAD
from alembic import op
import sqlalchemy as sa

=======
import sqlalchemy as sa

from alembic import op
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)

# revision identifiers, used by Alembic.
revision = "710f33c8368f"
down_revision = "90421e74de2b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("bots", sa.Column("channels_count", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bots", "channels_count")
    # ### end Alembic commands ###
