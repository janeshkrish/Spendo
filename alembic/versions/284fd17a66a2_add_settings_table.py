"""add settings table

Revision ID: 284fd17a66a2
Revises: 
Create Date: 2025-04-11 09:31:56.292700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '284fd17a66a2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('monthly_budget', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_settings_id'), 'settings', ['id'], unique=False)
    #op.alter_column('transactions', 'amount',
      #         existing_type=sa.FLOAT(),
       #        nullable=False)
    #op.alter_column('transactions', 'date',
     #          existing_type=sa.DATE(),
      #         nullable=False)
    #op.alter_column('transactions', 'category',
     #          existing_type=sa.VARCHAR(),
      #         nullable=False)
    #op.alter_column('transactions', 'merchant',
      #         existing_type=sa.VARCHAR(),
       #        nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'merchant',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('transactions', 'category',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('transactions', 'date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('transactions', 'amount',
               existing_type=sa.FLOAT(),
               nullable=True)
    op.drop_index(op.f('ix_settings_id'), table_name='settings')
    op.drop_table('settings')
    # ### end Alembic commands ###
