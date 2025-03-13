from flask import Blueprint, request, redirect, url_for, flash, render_template
from datetime import datetime
from models import db, Relatorio, Categoria, Produto

relatorio_bp = Blueprint('relatorio_bp', __name__)

def normalizar_nome_material(nome):
    """
    Normaliza o nome do material para os valores fixos:
      - "Filme"
      - "Cola Mel"
      - "Cola Una"
      - "Cola Kisafix"
      - "Pó para Pintura"
      - "EPS"
      - "Aço"
    Se o nome não corresponder a nenhum desses, retorna None.
    """
    nome_lower = nome.lower()
    if "filme" in nome_lower:
        return "Filme"
    elif "cola mel" in nome_lower:
        return "Cola Mel"
    elif "cola una" in nome_lower:
        return "Cola Una"
    elif "cola kisafix" in nome_lower:
        return "Cola Kisafix"
    elif "pó" in nome_lower or "pintura" in nome_lower:
        return "Pó para Pintura"
    elif "eps" in nome_lower:
        return "EPS"
    elif "aço" in nome_lower:
        return "Aço"
    else:
        return None

# Mapeamento de tarefas para o nome da categoria fixa correspondente
task_to_category = {
    "Colagem de Filme (Normal)": "Filme",
    "Pintura Eletrostática": "Pó para Pintura",
    "Colagem de Cola Mel": "Cola Mel"
    # Adicione outras tarefas conforme necessário.
}

@relatorio_bp.route('/', methods=['POST'])
def processar_formulario():
    # Extrair dados do formulário
    nome_cliente = request.form.get("nomeCliente")
    horario_inicio_str = request.form.get("horarioInicio")
    tarefa = request.form.get("tarefa")
    metros_quadrados_str = request.form.get("metrosQuadrados")
    horario_fim_str = request.form.get("horarioFim")

    # Conversão de horários para datetime.time
    try:
        horario_inicio = datetime.strptime(horario_inicio_str, "%H:%M").time()
    except (ValueError, TypeError):
        flash("Horário de início inválido.", "error")
        return redirect(url_for('relatorio_bp.tabela'))

    try:
        horario_fim = datetime.strptime(horario_fim_str, "%H:%M").time()
    except (ValueError, TypeError):
        flash("Horário de fim inválido.", "error")
        return redirect(url_for('relatorio_bp.tabela'))

    # Converter metros quadrados para float
    try:
        metros_quadrados = float(metros_quadrados_str)
    except (ValueError, TypeError):
        metros_quadrados = 0.0

    # Extrair e normalizar os dados dos materiais gastos (inputs que começam com "material_")
    materiais = {}
    for key, value in request.form.items():
        if key.startswith("material_"):
            material_original = key.replace("material_", "")
            material_normalizado = normalizar_nome_material(material_original)
            # Se não reconhecer o material, ignora-o
            if material_normalizado is None:
                continue
            try:
                gasto = float(value)
                if material_normalizado in materiais:
                    materiais[material_normalizado] += gasto
                else:
                    materiais[material_normalizado] = gasto
            except (ValueError, TypeError):
                if material_normalizado not in materiais:
                    materiais[material_normalizado] = 0.0

    # Usa o mapeamento de tarefa para determinar a categoria fixa correspondente.
    # Se a tarefa não estiver mapeada, utiliza o próprio valor da tarefa.
    categoria_nome = task_to_category.get(tarefa, tarefa)
    categoria = Categoria.query.filter_by(nome=categoria_nome).first()
    
    if categoria:
        for material_nome, gasto in materiais.items():
            # Busca o produto associado à categoria fixa cujo nome corresponda ao material normalizado
            produto = Produto.query.filter_by(nome=material_nome, categoria=categoria).first()
            if produto:
                produto.quantidade_atual -= gasto * metros_quadrados
                if produto.quantidade_atual < 0:
                    produto.quantidade_atual = 0
        # Atualiza o campo quantidade_total da categoria com base na soma dos produtos
        categoria.quantidade_total = categoria.contar_produtos()
        db.session.commit()

    # Cria a instância do relatório e salva no banco de dados
    novo_relatorio = Relatorio(
        nome_cliente=nome_cliente,
        horario_inicio=horario_inicio,
        tarefa=tarefa,
        materiais_gastos=materiais,
        metros_quadrados=metros_quadrados,
        horario_fim=horario_fim
    )
    db.session.add(novo_relatorio)
    db.session.commit()

    flash("Relatório salvo com sucesso!", "success")
    return redirect(url_for('relatorio_bp.tabela'))

@relatorio_bp.route('/tabela')
def tabela():
    relatorios = Relatorio.query.order_by(Relatorio.criado_em.desc()).all()
    return render_template("tabela.html", relatorios=relatorios)
