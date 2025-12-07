"""enforce not null constraints

Revision ID: 11cc3388b040
Revises: aa9924f40b56
Create Date: 2025-12-04 19:41:18.689301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11cc3388b040'
down_revision: Union[str, Sequence[str], None] = 'aa9924f40b56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
