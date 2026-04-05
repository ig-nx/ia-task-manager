"""create todos table

Revision ID: 8fb8217edc35
Revises: 
Create Date: 2026-01-23 08:19:16.679931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fb8217edc35'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    create table todos(
        id bigserial primary key,
        name text,
        completed boolean not null default false
    )
    """)

def downgrade():
    op.execute("drop table todos;")
