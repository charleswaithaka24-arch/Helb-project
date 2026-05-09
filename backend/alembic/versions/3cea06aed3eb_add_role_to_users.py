"""add role to users

Revision ID: 3cea06aed3eb
Revises: add_helb_budget_tables
Create Date: 2026-05-09 14:12:07.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cea06aed3eb'
down_revision = 'add_helb_budget_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add role column to users table
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, default='student'))


def downgrade() -> None:
    # Remove role column from users table
    op.drop_column('users', 'role')
