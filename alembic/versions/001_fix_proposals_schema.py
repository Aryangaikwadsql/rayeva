"""Fix proposals table schema - add missing columns."""

# revision identifiers, this is what's used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add customer_phone if not exists
    op.add_column('proposals', sa.Column('customer_phone', sa.String(), nullable=True))
    
    # Create index safely
    op.execute('CREATE INDEX IF NOT EXISTS "ix_proposals_customer_phone" ON proposals (customer_phone)')
    
    # Add status if not exists
op.add_column('proposals', sa.Column('status', sa.String(), server_default='PENDING', nullable=False))
    
    # Add updated_at if not exists
    op.add_column('proposals', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

def downgrade():
    op.drop_column('proposals', 'updated_at')
    op.drop_column('proposals', 'status')
    op.drop_column('proposals', 'customer_phone')
    op.execute('DROP INDEX IF EXISTS "ix_proposals_customer_phone"')
