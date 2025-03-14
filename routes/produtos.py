from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Produto, Unidade, db, Categoria, CATEGORIAS_PREDEFINIDAS

# Cria o Blueprint para Produtos
produtos_bp = Blueprint('produtos', __name__)

def get_categorias_predefinidas():
    # Retorna somente as categorias cujos nomes estão no dicionário de categorias pré-definidas
    return Categoria.query.filter(Categoria.nome.in_(list(CATEGORIAS_PREDEFINIDAS.keys()))).all()

# Rota para listar produtos: acessível em /produtos/
@produtos_bp.route('/')
def listar_produtos():
    try:
        produtos = Produto.query.all()
        categorias = get_categorias_predefinidas()
        # Obter a contagem de produtos por categoria
        contagem_por_categoria = {categoria.id: categoria.contar_produtos() for categoria in categorias}
        return render_template(
            'produtos.html',
            produtos=produtos,
            categorias=categorias,
            contagem_por_categoria=contagem_por_categoria
        )
    except Exception as e:
        flash(f'Erro ao listar produtos: {str(e)}', 'danger')
        return render_template('produtos.html', produtos=[], categorias=[], contagem_por_categoria={})

# Rota para criar um novo produto: acessível em /produtos/novo
@produtos_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    categorias = get_categorias_predefinidas()
    unidades = Unidade.query.all()
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        descricao = request.form.get('descricao')
        unidade_id = request.form.get('unidade_id')
        categoria_id = request.form.get('categoria_id')

        # Validação simples: todos os campos obrigatórios devem ser preenchidos
        if not nome or not preco or not quantidade or not unidade_id or not categoria_id:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('novo_produto.html', form_data=request.form, categorias=categorias, unidades=unidades)

        # Validação para garantir que a categoria selecionada é uma das pré-definidas
        seeded_category_ids = [str(c.id) for c in categorias]
        if categoria_id not in seeded_category_ids:
            flash('Selecione uma categoria válida.', 'danger')
            return render_template('novo_produto.html', form_data=request.form, categorias=categorias, unidades=unidades)

        try:
            novo_produto = Produto(
                nome=nome,
                preco=preco,
                quantidade_atual=quantidade,
                descricao=descricao,
                unidade_id=unidade_id,
                categoria_id=categoria_id
            )
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('produtos.listar_produtos'))
        except Exception as e:
            flash(f'Erro ao adicionar produto: {str(e)}', 'danger')
            db.session.rollback()
            return render_template('novo_produto.html', form_data=request.form, categorias=categorias, unidades=unidades)

    return render_template('novo_produto.html', form_data={}, categorias=categorias, unidades=unidades)

# Rota para editar um produto: acessível em /produtos/editar/<id>
@produtos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    categorias = get_categorias_predefinidas()
    unidades = Unidade.query.all()
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        descricao = request.form.get('descricao')
        unidade_id = request.form.get('unidade_id')
        categoria_id = request.form.get('categoria_id')

        if not nome or not preco or not quantidade or not unidade_id or not categoria_id:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('editar_produto.html', produto=produto, form_data=request.form, categorias=categorias, unidades=unidades)

        # Validação para garantir que a categoria selecionada é uma das pré-definidas
        seeded_category_ids = [str(c.id) for c in categorias]
        if categoria_id not in seeded_category_ids:
            flash('Selecione uma categoria válida.', 'danger')
            return render_template('editar_produto.html', produto=produto, form_data=request.form, categorias=categorias, unidades=unidades)

        try:
            produto.nome = nome
            produto.preco = preco
            produto.quantidade_atual = quantidade
            produto.descricao = descricao
            produto.unidade_id = unidade_id
            produto.categoria_id = categoria_id
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('produtos.listar_produtos'))
        except Exception as e:
            flash(f'Erro ao atualizar produto: {str(e)}', 'danger')
            db.session.rollback()
            return render_template('editar_produto.html', produto=produto, form_data=request.form, categorias=categorias, unidades=unidades)

    return render_template('editar_produto.html', produto=produto, form_data={}, categorias=categorias, unidades=unidades)

# Rota para deletar um produto: acessível em /produtos/deletar/<id>
@produtos_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    try:
        db.session.delete(produto)
        db.session.commit()
        flash('Produto removido com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao remover produto: {str(e)}', 'danger')
        db.session.rollback()
    return redirect(url_for('produtos.listar_produtos'))
