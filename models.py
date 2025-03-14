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
    unidade = db.relationship('Unidade', backref='produtos')

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