"""Initial migration

Revision ID: b796013499e3
Revises: 4ea27e9c38b9
Create Date: 2024-06-01 17:58:23.553412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b796013499e3'
down_revision: Union[str, None] = '4ea27e9c38b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clan_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clan_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['clan_id'], ['clan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('clan', 'count_score')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clan', sa.Column('count_score', sa.INTEGER(), nullable=False))
    op.drop_table('clan_score')
    # ### end Alembic commands ###
