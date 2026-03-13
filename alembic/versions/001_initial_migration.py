r"""Initial migration."""

# revision identifiers, this is what's used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

def upgrade():
    # Add missing columns to existing proposals table (products exists from create_all)
    op.add_column('proposals', sa.Column('customer_phone', sa.String(), nullable=True))
    op.execute('CREATE INDEX IF NOT EXISTS ix_proposals_customer_phone ON proposals (customer_phone)')
    
    # Add status if missing (fallback to String)
op.add_column('proposals', sa.Column('status', sa.String(), nullable=False, server_default='PENDING'))
    
    # Add updated_at if missing
    op.add_column('proposals', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_needs', sa.String(), nullable=False),
    sa.Column('budget', sa.Float(), nullable=False),
    sa.Column('products', sa.JSON(), nullable=True),
    sa.Column('budget_alloc', sa.JSON(), nullable=True),
    sa.Column('cost_breakdown', sa.JSON(), nullable=True),
    sa.Column('impact_summary', sa.String(), nullable=True),
    sa.Column('customer_phone', sa.String(), nullable=True),
sa.Column('status', sa.String(), nullable=False, server_default='PENDING'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_proposals_customer_phone'), 'proposals', ['customer_phone'], unique=False)

def downgrade():
    op.drop_column('proposals', 'updated_at')
    op.drop_column('proposals', 'status')
    op.execute('DROP INDEX IF EXISTS ix_proposals_customer_phone')
    op.drop_column('proposals', 'customer_phone')
