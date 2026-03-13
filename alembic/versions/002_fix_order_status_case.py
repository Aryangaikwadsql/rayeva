"""Fix order status case sensitivity - update 'pending' to 'PENDING' in DB."""

# revision identifiers
revision = '002_fix_order_status_case'
down_revision = '001_fix_proposals_schema'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.execute("UPDATE proposals SET status = 'PENDING' WHERE LOWER(status) = 'pending'")

def downgrade():
    op.execute("UPDATE proposals SET status = 'pending' WHERE status = 'PENDING'")

