from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Usuario, db
from flask_login import login_user, logout_user, login_required

# Define o blueprint com um nome único
usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        # Em produção, sempre utilize hash para senhas!
        usuario = Usuario.query.filter_by(nome=nome, senha=senha).first()
        if usuario:
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
            return redirect(url_for('usuarios_bp.login'))
    return render_template('login.html')

@usuarios_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('usuarios_bp.login'))

@usuarios_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        if senha != confirmar_senha:
            flash('As senhas não conferem.', 'danger')
            return redirect(url_for('usuarios_bp.cadastrar'))
        if Usuario.query.filter_by(email=email).first():
            flash('Já existe um usuário com este e-mail.', 'danger')
            return redirect(url_for('usuarios_bp.cadastrar'))
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, papel="usuario")
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('usuarios_bp.login'))
    return render_template('cadastro.html')
