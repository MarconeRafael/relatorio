from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Produto, Fornecedor, Categoria, db

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
        # Evite redirect loop; renderize a página com uma lista vazia
        return render_template('produtos.html', produtos=[])

# Rota para criar um novo produto: acessível em /produtos/novo
@produtos_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    # Consulta os fornecedores e categorias cadastrados para exibição no dropdown
    fornecedores = Fornecedor.query.all()
    categorias = Categoria.query.all()  # Adicionando a consulta para categorias
    if request.method == 'POST':
        # Coleta os dados do formulário
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        descricao = request.form.get('descricao')
        unidade = request.form.get('unidade')
        categoria_id = request.form.get('categoria_id')
        fornecedor_id = request.form.get('fornecedor_id')

        # Validação simples: somente os campos nome, preco, quantidade e unidade são obrigatórios
        if not nome or not preco or not quantidade or not unidade:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('novo_produto.html', form_data=request.form, fornecedores=fornecedores, categorias=categorias)

        try:
            novo_produto = Produto(
                codigo=codigo,
                nome=nome,
                preco=preco,
                quantidade_atual=quantidade,
                descricao=descricao,
                unidade=unidade,
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
            return render_template('novo_produto.html', form_data=request.form, fornecedores=fornecedores, categorias=categorias)

    # No GET, passa um dicionário vazio para form_data, a lista de fornecedores e categorias
    return render_template('novo_produto.html', form_data={}, fornecedores=fornecedores, categorias=categorias)

# Rota para editar um produto: acessível em /produtos/editar/<id>
@produtos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    fornecedores = Fornecedor.query.all()
    categorias = Categoria.query.all()  # Adicionando a consulta para categorias
    if request.method == 'POST':
        # Coleta os dados do formulário
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        descricao = request.form.get('descricao')
        unidade = request.form.get('unidade')
        categoria_id = request.form.get('categoria_id')
        fornecedor_id = request.form.get('fornecedor_id')

        # Validação simples dos campos obrigatórios
        if not nome or not preco or not quantidade or not unidade:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('editar_produto.html', produto=produto, form_data=request.form, fornecedores=fornecedores, categorias=categorias)

        try:
            produto.nome = nome
            produto.preco = preco
            produto.quantidade_atual = quantidade
            produto.descricao = descricao
            produto.unidade = unidade
            produto.categoria_id = categoria_id
            produto.fornecedor_id = fornecedor_id
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('produtos.listar_produtos'))
        except Exception as e:
            flash(f'Erro ao atualizar produto: {str(e)}', 'danger')
            db.session.rollback()
            return render_template('editar_produto.html', produto=produto, form_data=request.form, fornecedores=fornecedores, categorias=categorias)

    return render_template('editar_produto.html', produto=produto, form_data={}, fornecedores=fornecedores, categorias=categorias)

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
