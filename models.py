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
    # Flag para controle de notificação (ex: se já foi disparada uma notificação de estoque baixo)
    notificado = db.Column(db.Boolean, default=False)

    produtos = db.relationship('Produto', backref='categoria', lazy=True)

    def atualizar_quantidade_total(self):
        """
        Atualiza 'quantidade_total' com a soma das quantidades atuais dos produtos associados.
        Esse método pode ser utilizado para reinicializar o estoque a partir dos produtos cadastrados,
        antes de aplicar ajustes como materiais gastos.
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
        
        Atenção: Este método deve ser utilizado com cautela, garantindo que a redução
        seja aplicada apenas uma vez para cada relatório, para evitar subtrair repetidamente.
        
        As chaves do dicionário devem corresponder exatamente aos nomes das categorias.
        """
        if self.materiais_gastos:
            for categoria_nome, gasto in self.materiais_gastos.items():
                categoria = Categoria.query.filter_by(nome=categoria_nome).first()
                if categoria:
                    categoria.quantidade_total -= gasto

    def calcular_duracao(self):
        """
        Calcula a duração da tarefa em minutos.
        Converte os horários de início e fim (objetos do tipo time) para minutos e retorna a diferença.
        Caso a diferença seja negativa (tarefa que ultrapassa a meia-noite), ajusta adicionando 24 horas em minutos.
        """
        inicio = self.horario_inicio
        fim = self.horario_fim
        inicio_minutos = inicio.hour * 60 + inicio.minute
        fim_minutos = fim.hour * 60 + fim.minute
        duracao = fim_minutos - inicio_minutos
        if duracao < 0:
            duracao += 24 * 60
        return duracao

    def tempo_por_m2(self):
        """
        Calcula o tempo gasto por metro quadrado.
        Divide a duração da tarefa (em minutos) pelos metros quadrados trabalhados.
        Retorna None se 'metros_quadrados' for zero para evitar divisão por zero.
        """
        if self.metros_quadrados > 0:
            return self.calcular_duracao() / self.metros_quadrados
        else:
            return None

    def consumo_por_m2(self):
        """
        Calcula o consumo real por metro quadrado para cada material.
        Para cada material registrado em 'materiais_gastos', divide a quantidade gasta pelos metros quadrados.
        Retorna um dicionário com os materiais e o consumo por m².
        Se 'metros_quadrados' for zero ou 'materiais_gastos' for None, retorna um dicionário vazio.
        """
        if self.metros_quadrados > 0 and self.materiais_gastos:
            consumo = {}
            for material, gasto in self.materiais_gastos.items():
                consumo[material] = gasto / self.metros_quadrados
            return consumo
        else:
            return {}

# Dicionário com as categorias pré-definidas e seus valores mínimos
CATEGORIAS_PREDEFINIDAS = {
    "Filme branco": 1000,
    "Filme amadeirado": 1000,
    "Filme preto": 500,
    "Filme ultralight": 200,
    "Cola Mel": 200,
    "Cola Kisafix": 160,
    "Cola Una": 140,
    "Pó para Pintura branco": 150,
    "Pó para Pintura preto fosco": 50,
    "Pó para Pintura terracota": 50,
    "Pó para Pintura preto brilhoso": 25,
    "Pó para Pintura cinza": 10,
    "Pó para Pintura amarelo": 10,
    "Pó para Pintura vermelho": 10,
    "Parafuso autobrocante": 1000,
    "Parafuso costura": 50,
    "EPS": 1000,
    "cuminheeira": 1,
    "Aço": 1,
    "alcool": 5,
    "estilete": 15,
    "luvas": 100,
}

