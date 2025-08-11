"""make_company_id_nullable_in_invalidated_tokens

Revision ID: 928a2787e159
Revises: b6544a1c028a
Create Date: 2025-08-10 15:36:40.038586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '928a2787e159'
down_revision: Union[str, Sequence[str], None] = 'b6544a1c028a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Hacer company_id nullable en invalidated_tokens para permitir tokens de reset de contraseña
    op.alter_column('invalidated_tokens', 'company_id',
                    existing_type=sa.UUID(),
                    nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Revertir company_id a NOT NULL
    op.alter_column('invalidated_tokens', 'company_id',
                    existing_type=sa.UUID(),
                    nullable=False)
