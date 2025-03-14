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

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    # Estoque mínimo definido para a categoria
    quantidade_minima = db.Column(db.Float, nullable=False)
    # Estoque atual da categoria (inicialmente a soma dos produtos, depois ajustado conforme gastos)
    quantidade_total = db.Column(db.Float, default=0)
    # Flag para controle de notificação
    notificado = db.Column(db.Boolean, default=False)

    produtos = db.relationship('Produto', backref='categoria', lazy=True)

    def atualizar_quantidade_total(self):
        """
        Atualiza 'quantidade_total' com a soma das quantidades atuais dos produtos associados.
        Esse método pode ser usado para reinicializar o estoque a partir dos produtos cadastrados.
        """
        self.quantidade_total = sum(produto.quantidade_atual for produto in self.produtos)

    def contar_produtos(self):
        """Retorna o número de produtos associados à categoria."""
        return len(self.produtos)

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
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
    # Armazena um dicionário onde as chaves são os nomes das categorias e os valores são as quantidades a serem reduzidas
    materiais_gastos = db.Column(db.JSON)
    metros_quadrados = db.Column(db.Float, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def aplicar_materiais_gastos(self):
        """
        Percorre o dicionário 'materiais_gastos' e reduz a 'quantidade_total'
        da categoria correspondente com base no valor gasto.
        As chaves do dicionário devem corresponder aos nomes das categorias.
        """
        if self.materiais_gastos:
            for categoria_nome, gasto in self.materiais_gastos.items():
                categoria = Categoria.query.filter_by(nome=categoria_nome).first()
                if categoria:
                    categoria.quantidade_total -= gasto

# Dicionário com as categorias pré-definidas e seus valores mínimos
CATEGORIAS_PREDEFINIDAS = {
    'Filme': 10.0,
    'Cola Mel': 5.0,
    'Cola Una': 5.0,
    'Pó para Pintura': 8.0,
    'Cola Kisafix': 6.0,
    'EPS': 7.0,
    'Aço': 20.0,
}
