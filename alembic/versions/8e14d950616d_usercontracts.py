"""UserContracts

Revision ID: 8e14d950616d
Revises: 90c148f78235
Create Date: 2022-08-21 13:02:03.985072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e14d950616d'
down_revision = '90c148f78235'
branch_labels = None
depends_on = None


def upgrade() -> None:


    op.create_table(
        "contract_agreement",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("day", sa.Integer(), nullable=False),
        sa.Column("duration", sa.String(), nullable=False),
        sa.Column("total_amount", sa.Integer(), nullable=False),
        sa.Column("scheduled_amount", sa.Integer(), nullable=False),
        sa.Column("second_party_id", sa.Integer(), nullable= False),
        sa.Column("first_party_id", sa.Integer(), nullable= False),
        sa.Column("first_party_acceptance", sa.Boolean(), server_default= sa.text("true")),
        sa.Column("second_party_acceptance", sa.Boolean(), server_default= sa.text("true")),
        sa.Column("date_created",sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,),

        sa.ForeignKeyConstraint(["second_party_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["first_party_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )















    pass


def downgrade() -> None:
    op.drop_table("contract_agreement")
    pass
