"""Create views: user_company_roles_permissions, user_company_roles_permissions_filtered

Revision ID: 177d058d549e
Revises: 31b015770dbc
Create Date: 2025-08-05 13:23:08.469019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '177d058d549e'
down_revision: Union[str, Sequence[str], None] = '31b015770dbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
