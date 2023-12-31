"""fix nullable

Revision ID: 703d87820a95
Revises: 7ed92dc98c00
Create Date: 2023-12-12 22:16:56.294661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '703d87820a95'
down_revision: Union[str, None] = '7ed92dc98c00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Odds', 'first_handicap',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Odds', 'second_handicap',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Odds', 'second_handicap',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Odds', 'first_handicap',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
