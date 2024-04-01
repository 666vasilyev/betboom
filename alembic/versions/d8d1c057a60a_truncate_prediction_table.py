"""truncate prediction table

Revision ID: d8d1c057a60a
Revises: 0cf4292fddb3
Create Date: 2024-04-01 11:21:13.042055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd8d1c057a60a'
down_revision: Union[str, None] = '0cf4292fddb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Predictions')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Predictions',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Predictions_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('winner', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('bet', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('ratio', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('first_team', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('second_team', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Predictions_pkey')
    )
    # ### end Alembic commands ###
