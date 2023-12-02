"""Add message to ChannelBotBundles db

Revision ID: 9e6041f4cde4
Revises: 224244d30d47
Create Date: 2023-05-16 16:07:40.367853

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "9e6041f4cde4"
down_revision = "224244d30d47"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "ChannelBotBundles", sa.Column("message", sa.String(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("ChannelBotBundles", "message")
    # ### end Alembic commands ###