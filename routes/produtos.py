from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Produto, Fornecedor, Categoria, Unidade, db

# Cria o Blueprint para Produtos
produtos_bp = Blueprint('produtos', __name__)

# Rota para listar produtos: acessível em /produtos/
@produtos_bp.route('/')
def listar_produtos():
    try:
        produtos = Produto.query.all()
        return render_template('produtos.html', produtos=produtos)
    except Exception as e:
        flash(f'Erro ao listar produtos: {str(e)}', 'danger')
        return render_template('produtos.html', produtos=[])

# Rota para criar um novo produto: acessível em /produtos/novo
@produtos_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    fornecedores = Fornecedor.query.all()
    categorias = Categoria.query.all()
    unidades = Unidade.query.all()  # Adicionando a consulta para unidades
    
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        descricao = request.form.get('descricao')
        unidade_id = request.form.get('unidade_id')  # Mudança para usar a unidade_id
        categoria_id = request.form.get('categoria_id')
        fornecedor_id = request.form.get('fornecedor_id')

        if not nome or not preco or not quantidade or not unidade_id:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('novo_produto.html', form_data=request.form, fornecedores=fornecedores, categorias=categorias, unidades=unidades)

        try:
            novo_produto = Produto(
                codigo=codigo,
                nome=nome,
                preco=preco,
                quantidade_atual=quantidade,
                descricao=descricao,
                unidade_id=unidade_id,  # Mudança para usar unidade_id
                categoria_id=categoria_id,
                fornecedor_id=fornecedor_id
            )
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('produtos.listar_produtos'))
        except Exception as e:
            flash(f'Erro ao adicionar produto: {str(e)}', 'danger')
            db.session.rollback()
            return render_template('novo_produto.html', form_data=request.form, fornecedores=fornecedores, categorias=categorias, unidades=unidades)

    return render_template('novo_produto.html', form_data={}, fornecedores=fornecedores, categorias=categorias, unidades=unidades)

# Rota para editar um produto: acessível em /produtos/editar/<id>
@produtos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    fornecedores = Fornecedor.query.all()
    categorias = Categoria.query.all()
    unidades = Unidade.query.all()  # Adicionando a consulta para unidades
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        descricao = request.form.get('descricao')
        unidade_id = request.form.get('unidade_id')  # Mudança para usar a unidade_id
        categoria_id = request.form.get('categoria_id')
        fornecedor_id = request.form.get('fornecedor_id')

        if not nome or not preco or not quantidade or not unidade_id:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('editar_produto.html', produto=produto, form_data=request.form, fornecedores=fornecedores, categorias=categorias, unidades=unidades)

        try:
            produto.nome = nome
            produto.preco = preco
            produto.quantidade_atual = quantidade
            produto.descricao = descricao
            produto.unidade_id = unidade_id  # Mudança para usar unidade_id
            produto.categoria_id = categoria_id
            produto.fornecedor_id = fornecedor_id
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('produtos.listar_produtos'))
        except Exception as e:
            flash(f'Erro ao atualizar produto: {str(e)}', 'danger')
            db.session.rollback()
            return render_template('editar_produto.html', produto=produto, form_data=request.form, fornecedores=fornecedores, categorias=categorias, unidades=unidades)

    return render_template('editar_produto.html', produto=produto, form_data={}, fornecedores=fornecedores, categorias=categorias, unidades=unidades)

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
