# routes/categoria.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Categoria

# Cria o Blueprint para Categorias
categoria_bp = Blueprint('categorias_bp', __name__)

# Rota para exibir o formulário de cadastro
@categoria_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_categoria():
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        
        if not nome:
            flash("Nome da categoria é obrigatório!", "danger")
            return redirect(url_for('categorias_bp.cadastrar_categoria'))
        
        # Criar nova categoria
        nova_categoria = Categoria(nome=nome, descricao=descricao)
        
        # Adiciona ao banco de dados
        db.session.add(nova_categoria)
        db.session.commit()
        
        flash("Categoria cadastrada com sucesso!", "success")
        return redirect(url_for('categorias_bp.listar_categorias'))
    
    return render_template("cadastrar_categoria.html")


# Rota para listar todas as categorias
@categoria_bp.route("/listar")
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template("listar_categorias.html", categorias=categorias)


# Rota para editar uma categoria
@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    
    if request.method == 'POST':
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        
        if not nome:
            flash("Nome da categoria é obrigatório!", "danger")
            return render_template("editar_categoria.html", categoria=categoria)
        
        categoria.nome = nome
        categoria.descricao = descricao
        db.session.commit()
        
        flash("Categoria atualizada com sucesso!", "success")
        return redirect(url_for('categorias_bp.listar_categorias'))
    
    return render_template("editar_categoria.html", categoria=categoria)


# Rota para excluir uma categoria
@categoria_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    
    try:
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoria excluída com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao excluir categoria: {str(e)}", "danger")
        db.session.rollback()

    return redirect(url_for('categorias_bp.listar_categorias'))
