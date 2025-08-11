"""add is_verified to user

Revision ID: add_is_verified_to_user
Revises: 28186d2b3882
Create Date: 2025-01-27 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_is_verified_to_user'
down_revision: Union[str, Sequence[str], None] = '28186d2b3882'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar columna is_verified si no existe
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'app_user' AND column_name = 'is_verified'
            ) THEN
                ALTER TABLE app_user ADD COLUMN is_verified BOOLEAN NOT NULL DEFAULT false;
            END IF;
        END $$;
    """)
    
    # Crear índice para is_verified
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes 
                WHERE tablename = 'app_user' AND indexname = 'ix_app_user_verified'
            ) THEN
                CREATE INDEX ix_app_user_verified ON app_user (is_verified);
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar índice
    op.execute("DROP INDEX IF EXISTS ix_app_user_verified")
    
    # Eliminar columna
    op.execute("ALTER TABLE app_user DROP COLUMN IF EXISTS is_verified") 