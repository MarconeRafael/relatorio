from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Categoria

categoria_bp = Blueprint('categorias_bp', __name__)

# Lista das categorias fixas permitidas
FIXED_CATEGORIES = ["Filme", "Cola Mel", "Cola Una", "Pó para Pintura", "Cola Kisafix", "EPS", "Aço"]

# Rota para exibir o formulário de cadastro
@categoria_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_categoria():
    if request.method == "POST":
        nome = request.form.get("nome")
        quantidade_minima = request.form.get("quantidade_minima")
        
        if not nome:
            flash("Nome da categoria é obrigatório!", "danger")
            return redirect(url_for('categorias_bp.cadastrar_categoria'))
        
        # Verifica se o nome informado está entre as categorias fixas
        if nome not in FIXED_CATEGORIES:
            flash("Categoria inválida! As categorias fixas são: " + ", ".join(FIXED_CATEGORIES), "danger")
            return redirect(url_for('categorias_bp.cadastrar_categoria'))
        
        # Verifica se a categoria já existe
        existente = Categoria.query.filter_by(nome=nome).first()
        if existente:
            flash("Categoria já cadastrada!", "warning")
            return redirect(url_for('categorias_bp.listar_categorias'))
        
        # Criar nova categoria
        nova_categoria = Categoria(nome=nome, quantidade_minima=quantidade_minima)
        
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


# Rota para editar uma categoria (apenas quantidade mínima pode ser alterada)
@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    
    if request.method == 'POST':
        # Não permite alteração do nome da categoria fixa; apenas quantidade mínima é editada.
        quantidade_minima = request.form.get("quantidade_minima")
        categoria.quantidade_minima = quantidade_minima
        db.session.commit()
        
        flash("Categoria atualizada com sucesso!", "success")
        return redirect(url_for('categorias_bp.listar_categorias'))
    
    return render_template("editar_categoria.html", categoria=categoria)


# Rota para excluir uma categoria (desabilitada para categorias fixas)
@categoria_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_categoria(id):
    flash("Categorias fixas não podem ser excluídas!", "danger")
    return redirect(url_for('categorias_bp.listar_categorias'))
