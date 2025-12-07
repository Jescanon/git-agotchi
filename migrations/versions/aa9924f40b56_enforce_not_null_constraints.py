"""enforce not null constraints

Revision ID: aa9924f40b56
Revises: 74e40b4db9ea
Create Date: 2025-12-04 19:39:32.045646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa9924f40b56'
down_revision: Union[str, Sequence[str], None] = '74e40b4db9ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
