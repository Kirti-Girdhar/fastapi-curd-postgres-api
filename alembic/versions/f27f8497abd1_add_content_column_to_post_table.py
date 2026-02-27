"""add content column to post table

Revision ID: f27f8497abd1
Revises: 20c3657164d8
Create Date: 2026-02-26 11:19:16.344568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f27f8497abd1'
down_revision: Union[str, Sequence[str], None] = '20c3657164d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
