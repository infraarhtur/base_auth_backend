"""Create permission tables: role_permission, user_role

Revision ID: 31b015770dbc
Revises: 6b732f6dabcf
Create Date: 2025-08-05 13:22:49.850996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31b015770dbc'
down_revision: Union[str, Sequence[str], None] = '6b732f6dabcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
