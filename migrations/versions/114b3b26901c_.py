"""empty message

Revision ID: 114b3b26901c
Revises: 1563fa8433e3
Create Date: 2021-02-28 12:02:49.868920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '114b3b26901c'
down_revision = '1563fa8433e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ockovani_lide',
    sa.Column('datum', sa.Date(), nullable=False),
    sa.Column('vakcina', sa.Unicode(), nullable=False),
    sa.Column('kraj_nuts_kod', sa.Unicode(), nullable=True),
    sa.Column('kraj_nazev', sa.Unicode(), nullable=True),
    sa.Column('zarizeni_kod', sa.Unicode(), nullable=False),
    sa.Column('zarizeni_nazev', sa.Unicode(), nullable=True),
    sa.Column('poradi_davky', sa.Unicode(), nullable=False),
    sa.Column('vekova_skupina', sa.Unicode(), nullable=False),
    sa.Column('pocet', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('datum', 'vakcina', 'zarizeni_kod', 'poradi_davky', 'vekova_skupina')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ockovani_lide')
    # ### end Alembic commands ###
