"""Create relationship tables: company_user, role, user_identity

Revision ID: 6b732f6dabcf
Revises: 66c32d7a84dd
Create Date: 2025-08-05 13:22:17.951835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b732f6dabcf'
down_revision: Union[str, Sequence[str], None] = '66c32d7a84dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
