"""add_is_activate_to_company_user

Revision ID: a261655577d5
Revises: 28186d2b3882
Create Date: 2025-08-08 16:18:27.160830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a261655577d5'
down_revision: Union[str, Sequence[str], None] = '28186d2b3882'
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
