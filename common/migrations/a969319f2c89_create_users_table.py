"""create_users_table

Revision ID: a969319f2c89
Revises: dab367473f75
Create Date: 2026-04-19 11:53:31.826623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a969319f2c89'
down_revision: Union[str, Sequence[str], None] = 'dab367473f75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создаем только таблицу пользователей
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем только таблицу пользователей
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')