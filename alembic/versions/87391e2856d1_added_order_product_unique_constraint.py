"""Added order_product_unique constraint

Revision ID: 87391e2856d1
Revises: 146f8b0a23d2
Create Date: 2024-04-01 15:59:56.863965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87391e2856d1'
down_revision: Union[str, None] = '146f8b0a23d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        constraint_name="order_product_unique",
        table_name="order_product",
        columns=["order_id", "product_id"],
        schema="main",
    )


def downgrade() -> None:
    op.drop_constraint(
        constraint_name="order_product_unique",
        table_name="order_product",
        schema="main",
    )
