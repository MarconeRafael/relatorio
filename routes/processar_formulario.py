from flask import Blueprint, request, redirect, url_for, flash, render_template
from datetime import datetime
from models import db, Relatorio, Categoria, Produto, CATEGORIAS_PREDEFINIDAS

relatorio_bp = Blueprint('relatorio_bp', __name__)

def normalizar_nome_material(nome):
    """
    Normaliza o nome do material para que corresponda a uma das chaves definidas em CATEGORIAS_PREDEFINIDAS:
      - Filmes: "Filme branco", "Filme amadeirado", "Filme preto" ou "Filme ultralight"
      - Colas: "Cola Mel", "Cola Una" ou "Cola Kisafix"
      - Pós para Pintura: "Pó para Pintura branco", "Pó para Pintura preto fosco", 
        "Pó para Pintura terracota", "Pó para Pintura preto brilhoso", "Pó para Pintura cinza", 
        "Pó para Pintura amarelo" ou "Pó para Pintura vermelho"
      - Outros: "EPS", "Aço", "Parafuso autobrocante", "Parafuso costura", "cuminheeira",
        "alcool", "estilete" e "luvas"
    Retorna None se não corresponder a nenhum destes.
    """
    nome_lower = nome.lower()
    if "filme" in nome_lower:
        if "branco" in nome_lower:
            return "Filme branco"
        elif "amadeirado" in nome_lower:
            return "Filme amadeirado"
        elif "preto" in nome_lower:
            return "Filme preto"
        elif "ultralight" in nome_lower:
            return "Filme ultralight"
        else:
            return "Filme branco"  # valor padrão para filmes
    elif "cola mel" in nome_lower:
        return "Cola Mel"
    elif "cola una" in nome_lower:
        return "Cola Una"
    elif "cola kisafix" in nome_lower:
        return "Cola Kisafix"
    elif "pó" in nome_lower or "pintura" in nome_lower:
        if "branco" in nome_lower:
            return "Pó para Pintura branco"
        elif "preto" in nome_lower and "fosco" in nome_lower:
            return "Pó para Pintura preto fosco"
        elif "terracota" in nome_lower:
            return "Pó para Pintura terracota"
        elif "preto" in nome_lower and "brilhoso" in nome_lower:
            return "Pó para Pintura preto brilhoso"
        elif "cinza" in nome_lower:
            return "Pó para Pintura cinza"
        elif "amarelo" in nome_lower:
            return "Pó para Pintura amarelo"
        elif "vermelho" in nome_lower:
            return "Pó para Pintura vermelho"
        else:
            return "Pó para Pintura branco"  # valor padrão para pintura
    elif "eps" in nome_lower:
        return "EPS"
    elif "aço" in nome_lower:
        return "Aço"
    elif "parafuso autobrocante" in nome_lower:
        return "Parafuso autobrocante"
    elif "parafuso costura" in nome_lower:
        return "Parafuso costura"
    elif "cuminheeira" in nome_lower:
        return "cuminheeira"
    elif "alcool" in nome_lower:
        return "alcool"
    elif "estilete" in nome_lower:
        return "estilete"
    elif "luvas" in nome_lower:
        return "luvas"
    else:
        return None

# Mapeamento de tarefas para a categoria padrão, de acordo com os nomes atualizados
task_to_category = {
    "Colagem de Filme (Normal)": "Filme branco",
    "Pintura Eletrostática": "Pó para Pintura branco",
    "Colagem de Cola Mel": "Cola Mel"
    # Outras tarefas podem ser mapeadas conforme necessário.
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

    # Determina a categoria fixa com base na tarefa
    categoria_nome = task_to_category.get(tarefa, tarefa)
    categoria = Categoria.query.filter_by(nome=categoria_nome).first()

    if categoria:
        for material_nome, gasto in materiais.items():
            # Busca o produto associado à categoria cujo nome corresponda ao material normalizado
            produto = Produto.query.filter_by(nome=material_nome, categoria=categoria).first()
            if produto:
                produto.quantidade_atual -= gasto * metros_quadrados
                if produto.quantidade_atual < 0:
                    produto.quantidade_atual = 0
        # Atualiza a quantidade total da categoria com base nos produtos associados
        categoria.atualizar_quantidade_total()
        db.session.commit()

    # Cria e salva o relatório
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
    return redirect(url_for('dashboard'))

@relatorio_bp.route('/tabela')
def tabela():
    relatorios = Relatorio.query.order_by(Relatorio.criado_em.desc()).all()
    return render_template("tabela.html", relatorios=relatorios)
