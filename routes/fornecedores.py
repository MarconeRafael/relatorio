from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Fornecedor, db

fornecedores_bp = Blueprint('fornecedores', __name__)

# Rota para listar fornecedores: acessível em /fornecedores/
@fornecedores_bp.route('/')
def listar_fornecedores():
    try:
        fornecedores = Fornecedor.query.all()
    except Exception as e:
        flash(f'Erro ao listar fornecedores: {str(e)}', 'danger')
        fornecedores = []
    return render_template('fornecedores.html', fornecedores=fornecedores)

# Rota para criar um novo fornecedor: acessível em /fornecedores/novo
@fornecedores_bp.route('/novo', methods=['GET', 'POST'])
def novo_fornecedor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        contato = request.form.get('contato')
        endereco = request.form.get('endereco')

        # Validação simples: somente o nome é obrigatório
        if not nome:
            flash('O nome é obrigatório.', 'danger')
            return render_template('novo_fornecedor.html', form_data=request.form)
        
        try:
            novo_fornecedor = Fornecedor(
                nome=nome,
                contato=contato,
                endereco=endereco
            )
            db.session.add(novo_fornecedor)
            db.session.commit()
            flash('Fornecedor adicionado com sucesso!', 'success')
            return redirect(url_for('fornecedores.listar_fornecedores'))
        except Exception as e:
            flash(f'Erro ao adicionar fornecedor: {str(e)}', 'danger')
            db.session.rollback()
            return render_template('novo_fornecedor.html', form_data=request.form)

    return render_template('novo_fornecedor.html', form_data={})

# Rota para editar um fornecedor: acessível em /fornecedores/editar/<id>
@fornecedores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        contato = request.form.get('contato')
        endereco = request.form.get('endereco')

        # Validação simples: nome é obrigatório
        if not nome:
            flash('O nome é obrigatório.', 'danger')
            return render_template('editar_fornecedor.html', fornecedor=fornecedor, form_data=request.form)

        try:
            fornecedor.nome = nome
            fornecedor.contato = contato
            fornecedor.endereco = endereco
            db.session.commit()
            flash('Fornecedor atualizado com sucesso!', 'success')
            return redirect(url_for('fornecedores.listar_fornecedores'))
        except Exception as e:
            flash(f'Erro ao atualizar fornecedor: {str(e)}', 'danger')
            db.session.rollback()
            return render_template('editar_fornecedor.html', fornecedor=fornecedor, form_data=request.form)

    return render_template('editar_fornecedor.html', fornecedor=fornecedor, form_data={})

# Rota para deletar um fornecedor: acessível em /fornecedores/deletar/<id>
@fornecedores_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    try:
        db.session.delete(fornecedor)
        db.session.commit()
        flash('Fornecedor removido com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao remover fornecedor: {str(e)}', 'danger')
        db.session.rollback()
    return redirect(url_for('fornecedores.listar_fornecedores'))
