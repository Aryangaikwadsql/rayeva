"""${message}

Revision ID: ${repr(revision_id)}
Revises: ${repr(parent_revision_id)}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers
revision = '${revision_id}'
down_revision = ${repr(parent_revision_id) or 'None'}
branch_labels = ${repr(branch_labels) or 'None'}
depends_on = ${repr(depends_on) or 'None'}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}

