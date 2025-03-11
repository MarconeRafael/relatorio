# routes/unidades.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Unidade, db

# Cria o Blueprint para Unidades
unidades_bp = Blueprint('unidades_bp', __name__)

# Rota para listar as unidades: acessível em /unidades/
@unidades_bp.route('/')
def listar_unidades():
    unidades = Unidade.query.all()
    return render_template('listar_unidades.html', unidades=unidades)

# Rota para cadastrar uma nova unidade: acessível em /unidades/cadastrar
@unidades_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_unidade():
    if request.method == 'POST':
        nome = request.form.get('nome')

        if not nome:
            flash('O nome da unidade é obrigatório!', 'danger')
            return render_template('cadastrar_unidade.html')

        try:
            nova_unidade = Unidade(nome=nome)
            db.session.add(nova_unidade)
            db.session.commit()
            flash('Unidade cadastrada com sucesso!', 'success')
            return redirect(url_for('unidades_bp.listar_unidades'))
        except Exception as e:
            flash(f'Erro ao cadastrar unidade: {str(e)}', 'danger')
            db.session.rollback()

    return render_template('cadastrar_unidade.html')

# Rota para editar uma unidade: acessível em /unidades/editar/<id>
@unidades_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_unidade(id):
    unidade = Unidade.query.get_or_404(id)
    
    if request.method == 'POST':
        nome = request.form.get('nome')

        if not nome:
            flash('O nome da unidade é obrigatório!', 'danger')
            return render_template('editar_unidade.html', unidade=unidade)

        try:
            unidade.nome = nome
            db.session.commit()
            flash('Unidade atualizada com sucesso!', 'success')
            return redirect(url_for('unidades_bp.listar_unidades'))
        except Exception as e:
            flash(f'Erro ao atualizar unidade: {str(e)}', 'danger')
            db.session.rollback()

    return render_template('editar_unidade.html', unidade=unidade)

# Rota para excluir uma unidade: acessível em /unidades/excluir/<id>
@unidades_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_unidade(id):
    unidade = Unidade.query.get_or_404(id)
    
    try:
        db.session.delete(unidade)
        db.session.commit()
        flash('Unidade excluída com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir unidade: {str(e)}', 'danger')
        db.session.rollback()

    return redirect(url_for('unidades_bp.listar_unidades'))
