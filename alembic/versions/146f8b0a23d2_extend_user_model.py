"""Extend User model

Revision ID: 146f8b0a23d2
Revises: 0d6be5fc027e
Create Date: 2024-03-29 11:16:51.275593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '146f8b0a23d2'
down_revision: Union[str, None] = '0d6be5fc027e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
