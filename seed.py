from app import app
from models import db, Categoria

# Lista de categorias de teste
CATEGORIAS_TESTE = [
    {"nome": "Materiais de Escritório", "quantidade_minima": 10},
    {"nome": "Equipamentos de Proteção", "quantidade_minima": 5},
    {"nome": "Insumos de Produção", "quantidade_minima": 20},
    {"nome": "Ferramentas Manuais", "quantidade_minima": 3},
    {"nome": "Produtos de Limpeza", "quantidade_minima": 8},
]

with app.app_context():
    for cat in CATEGORIAS_TESTE:
        existente = Categoria.query.filter_by(nome=cat["nome"]).first()
        if not existente:
            nova = Categoria(nome=cat["nome"], quantidade_minima=cat["quantidade_minima"])
            db.session.add(nova)

    db.session.commit()
    print("✅ Categorias de teste inseridas com sucesso!")
