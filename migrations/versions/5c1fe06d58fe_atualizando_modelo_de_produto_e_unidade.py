"""Atualizando modelo de Produto e Unidade

Revision ID: 5c1fe06d58fe
Revises: a9e970d0b413
Create Date: 2025-03-11 12:07:35.934262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c1fe06d58fe'
down_revision = 'a9e970d0b413'
branch_labels = None
depends_on = None


def upgrade():
    # Criação da tabela 'unidade'
    op.create_table('unidade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    
    # Alteração da tabela 'produto' para adicionar a coluna 'unidade_id' e a chave estrangeira
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unidade_id', sa.Integer(), nullable=False))
        # Nomeando explicitamente a constraint da chave estrangeira
        batch_op.create_foreign_key('fk_produto_unidade', 'unidade', ['unidade_id'], ['id'])
        batch_op.drop_column('unidade')  # Remover a coluna antiga 'unidade' que era uma string

def downgrade():
    # Reversão da migração: remove a chave estrangeira e restaura a coluna 'unidade' original
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unidade', sa.VARCHAR(length=20), nullable=True))
        batch_op.drop_constraint('fk_produto_unidade', type_='foreignkey')  # Remover a constraint 'fk_produto_unidade'
        batch_op.drop_column('unidade_id')

    # Exclui a tabela 'unidade'
    op.drop_table('unidade')
