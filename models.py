from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    papel = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.email})>'

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    quantidade_minima = db.Column(db.Float, default=0)
    quantidade_total = db.Column(db.Float, default=0)
    notificado = db.Column(db.Boolean, default=False)
    produtos = db.relationship('Produto', back_populates='categoria', lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('nome', name='uq_categoria_nome'),
    )

    def contar_produtos(self):
        return sum(produto.quantidade_atual for produto in self.produtos.all())

    def atualizar_quantidade_total(self):
        self.quantidade_total = self.contar_produtos()

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Unidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Unidade {self.nome}>'

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade.id'), nullable=False)
    quantidade_atual = db.Column(db.Float, default=0)
    preco = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)
    unidade = db.relationship('Unidade', backref='produtos')
    categoria = db.relationship('Categoria', back_populates='produtos')

    def __repr__(self):
        return f'<Produto {self.nome} (ID: {self.id})>'

class Relatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(100), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    tarefa = db.Column(db.String(150), nullable=False)
    materiais_gastos = db.Column(db.JSON)  # Armazena um dicionário com os materiais e quantidades
    metros_quadrados = db.Column(db.Float, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

def seed_categorias():
    """
    Insere as categorias pré-definidas no banco de dados, caso elas ainda não existam.
    Essa função pode ser chamada logo após a criação do banco ou via script de migração.
    """
    categorias_padrao = [
        'Filme', 
        'Cola Mel', 
        'Cola Una', 
        'Pó para Pintura', 
        'Cola Kisafix', 
        'EPS', 
        'Aço'
    ]
    for nome in categorias_padrao:
        if not Categoria.query.filter_by(nome=nome).first():
            nova_categoria = Categoria(nome=nome)
            db.session.add(nova_categoria)
    db.session.commit()
