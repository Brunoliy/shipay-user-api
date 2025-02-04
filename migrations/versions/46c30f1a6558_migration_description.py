"""migration description

Revision ID: 46c30f1a6558
Revises: 
Create Date: 2025-02-02 20:19:01.724113

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '46c30f1a6558'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Criar tabela roles
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, nullable=False)
    )

    # Inserir dados na tabela roles
    op.execute("""
        INSERT INTO roles (id, description) VALUES 
        (1, 'Admin'),
        (2, 'Manager'),
        (3, 'User'),
        (4, 'Guest'),
        (5, 'Support'),
        (6, 'Developer'),
        (7, 'QA'),
        (8, 'Moderator'),
        (9, 'Sales'),
        (10, 'Customer Success');
    """)

    # Criar tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id'), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=datetime.utcnow)
    )

    # Criar tabela claims
    op.create_table(
        'claims',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('active', sa.Boolean, nullable=False, server_default=sa.text("true"))
    )

    # Inserir dados na tabela claims
    op.execute("""
        INSERT INTO claims (id, description, active) VALUES 
        (1, 'View_Dashboard', true),
        (2, 'Edit_User', true),
        (3, 'Delete_User', true),
        (4, 'Manage_Roles', true),
        (5, 'Access_Reports', true),
        (6, 'Create_Content', true),
        (7, 'Edit_Content', true),
        (8, 'Delete_Content', true),
        (9, 'View_Logs', true),
        (10, 'Manage_Settings', true);
    """)

    # Criar tabela user_claim (relação entre users e claims)
    op.create_table(
        'user_claims',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
        sa.Column('claim_id', sa.Integer, sa.ForeignKey('claims.id', ondelete="CASCADE"), primary_key=True)
    )

def downgrade() -> None:
    # Deletar tabelas na ordem inversa para evitar problemas de chave estrangeira
    op.drop_table('user_claims')
    op.drop_table('claims')
    op.drop_table('users')
    op.drop_table('roles')
