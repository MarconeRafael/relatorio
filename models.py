from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

# Inicializa o SQLAlchemy sem passar a aplicação diretamente
db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    papel = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.email})>'


class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    contato = db.Column(db.String(100))
    endereco = db.Column(db.Text)
    produtos = db.relationship('Produto', backref='fornecedor', lazy=True)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nome}>'


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    unidade = db.Column(db.String(20))
    quantidade_atual = db.Column(db.Float, default=0)
    preco = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=True)
    movimentacoes = db.relationship('Movimentacao', backref='produto_movimentacoes', lazy=True)  # Alterado o backref para evitar conflito

    def __repr__(self):
        return f'<Produto {self.nome} (Código: {self.codigo})>'

    def registrar_movimentacao(self, tipo, quantidade, usuario_id=None, observacao=None):
        movimentacao = Movimentacao(
            produto_id=self.id,
            tipo=tipo,
            quantidade=quantidade,
            usuario_id=usuario_id,
            observacao=observacao
        )
        db.session.add(movimentacao)
        self.quantidade_atual += quantidade if tipo == 'entrada' else -quantidade
        db.session.commit()


class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    observacao = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    usuario = db.relationship('Usuario', backref='movimentacoes', lazy=True)
    produto = db.relationship('Produto', backref='movimentacoes_relacionadas', lazy=True)  # Alterado o backref para evitar conflito

    def __repr__(self):
        return f'<Movimentacao {self.tipo} de {self.quantidade} (Produto ID: {self.produto_id})>'
