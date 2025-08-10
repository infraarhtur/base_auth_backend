"""merge multiple heads

Revision ID: b6544a1c028a
Revises: add_is_verified_to_user, decb2109c704
Create Date: 2025-08-10 12:22:20.843659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6544a1c028a'
down_revision: Union[str, Sequence[str], None] = ('add_is_verified_to_user', 'decb2109c704')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
