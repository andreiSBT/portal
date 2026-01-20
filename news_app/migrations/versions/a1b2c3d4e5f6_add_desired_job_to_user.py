"""Add desired_job to user

Revision ID: a1b2c3d4e5f6
Revises: 8cc9c378d8d9
Create Date: 2026-01-17 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '8cc9c378d8d9'
branch_labels = None
depends_on = None


def upgrade():
    # Add desired_job column to users table
    op.add_column('users', sa.Column('desired_job', sa.String(length=50), nullable=True))


def downgrade():
    # Remove desired_job column from users table
    op.drop_column('users', 'desired_job')
