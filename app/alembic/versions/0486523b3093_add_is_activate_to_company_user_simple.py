"""add_is_activate_to_company_user_simple

Revision ID: 0486523b3093
Revises: a261655577d5
Create Date: 2025-08-08 16:45:12.160830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0486523b3093'
down_revision: Union[str, Sequence[str], None] = 'a261655577d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar campo is_activate a la tabla company_user
    op.add_column('company_user', sa.Column('is_activate', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar campo is_activate de la tabla company_user
    op.drop_column('company_user', 'is_activate')
