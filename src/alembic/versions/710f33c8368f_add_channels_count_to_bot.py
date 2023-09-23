"""add 'channels_count' to Bot

Revision ID: 710f33c8368f
Revises: 90421e74de2b
Create Date: 2023-05-12 12:11:58.568305

"""
import sqlalchemy as sa

from alembic import op

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
