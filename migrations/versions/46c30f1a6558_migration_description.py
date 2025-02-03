"""migration description

Revision ID: 46c30f1a6558
Revises: 
Create Date: 2025-02-02 20:19:01.724113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46c30f1a6558'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Criar tabela roles
    op.create_table(
        'roles',
        sa.Column('role_id', sa.Integer, primary_key=True, index=True),
        sa.Column('role_description', sa.String, nullable=False)
    )

    # Criar tabela users
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_name', sa.String, nullable=False),
        sa.Column('user_email', sa.String, nullable=False),
        sa.Column('user_password', sa.String, nullable=False),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.role_id'), nullable=False)
    )

    # Criar tabela claims
    op.create_table(
        'claims',
        sa.Column('claim_id', sa.Integer, primary_key=True, index=True),
        sa.Column('claim_description', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True)
    )

    # Criar tabela user_claims (relação entre users e claims)
    op.create_table(
        'user_claims',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id'), primary_key=True),
        sa.Column('claim_id', sa.Integer, sa.ForeignKey('claims.claim_id'), primary_key=True)
    )

def downgrade() -> None:
    # Deletar tabelas na ordem inversa para evitar problemas de chave estrangeira
    op.drop_table('user_claims')
    op.drop_table('claims')
    op.drop_table('users')
    op.drop_table('roles')
