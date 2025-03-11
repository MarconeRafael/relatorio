"""Removendo fornecedores

Revision ID: eb82e03b8c03
Revises: 5c1fe06d58fe
Create Date: 2025-03-11 HH:MM:SS

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eb82e03b8c03'
down_revision = '5c1fe06d58fe'
branch_labels = None
depends_on = None

def upgrade():
    # Remover a coluna 'fornecedor_id' da tabela 'produto'
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.drop_column('fornecedor_id')
    
    # Descarta a tabela 'fornecedor' se ela existir (não irá gerar erro se já não existir)
    op.execute("DROP TABLE IF EXISTS fornecedor")

def downgrade():
    # Recriar a tabela 'fornecedor'
    op.create_table(
        'fornecedor',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=150), nullable=False),
        sa.Column('contato', sa.String(length=100)),
        sa.Column('endereco', sa.Text),
        sa.PrimaryKeyConstraint('id')
    )
    # Re-adicionar a coluna 'fornecedor_id' na tabela 'produto' e criar a chave estrangeira
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fornecedor_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_produto_fornecedor', 'fornecedor', ['fornecedor_id'], ['id'])
