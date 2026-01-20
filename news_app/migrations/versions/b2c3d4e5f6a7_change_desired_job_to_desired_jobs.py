"""Change desired_job to desired_jobs

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-18 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Rename column from desired_job to desired_jobs and change type to Text
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('desired_jobs', sa.Text(), nullable=True))

    # Migrate existing data: convert single job to JSON array
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE users
        SET desired_jobs = '["' || desired_job || '"]'
        WHERE desired_job IS NOT NULL
    """))

    # Drop old column
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('desired_job')


def downgrade():
    # Add back old column
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('desired_job', sa.String(length=50), nullable=True))

    # Migrate data back: take first job from JSON array
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE users
        SET desired_job = (
            SELECT json_extract(desired_jobs, '$[0]')
            WHERE desired_jobs IS NOT NULL
        )
    """))

    # Drop new column
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('desired_jobs')
