from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Movimentacao, Produto, db
from flask_login import current_user

movimentacoes_bp = Blueprint('movimentacoes', __name__)

@movimentacoes_bp.route('/')
def listar_movimentacoes():
    try:
        # Lista todas as movimentações
        movimentacoes = Movimentacao.query.all()
        return render_template('movimentacoes.html', movimentacoes=movimentacoes)
    except Exception as e:
        # Caso haja erro, exibe a mensagem
        flash(f'Erro ao listar movimentações: {str(e)}', 'danger')
        return redirect(url_for('movimentacoes.listar_movimentacoes'))

# Alteração para capturar dados do corpo da requisição em formato JSON
@movimentacoes_bp.route('/registrar_automatico', methods=['POST'])
def registrar_movimentacao_automatica():
    try:
        # Captura os dados do corpo da requisição como JSON
        dados = request.get_json()

        # Coleta os dados da movimentação
        produto_id = dados.get('produto_id')
        quantidade = float(dados.get('quantidade'))  # Garantir que seja float
        tipo = dados.get('tipo')
        observacao = dados.get('observacao', '')  # Observação é opcional

        # Validação do tipo de movimentação
        if tipo not in ['entrada', 'saida']:  
            flash('Tipo de movimentação inválido. Use "entrada" ou "saida".', 'danger')
            return {'message': 'Erro: Tipo de movimentação inválido.'}, 400

        # Validação de quantidade e produto
        if not produto_id or quantidade <= 0:
            flash('Produto e quantidade inválidos.', 'danger')
            return {'message': 'Erro: Produto ou quantidade inválidos.'}, 400

        # Associar a movimentação ao usuário atual, caso esteja autenticado
        usuario_id = current_user.id if current_user.is_authenticated else None

        # Criação do objeto de movimentação automaticamente
        produto = Produto.query.get(produto_id)
        if produto:
            # Registrar a movimentação no banco
            movimentacao = Movimentacao(
                produto_id=produto_id,
                tipo=tipo,
                quantidade=quantidade,
                observacao=observacao,
                usuario_id=usuario_id  # Relacionando ao usuário que fez a movimentação
            )
            
            # Adicionar e salvar no banco
            db.session.add(movimentacao)
            db.session.commit()
            flash(f'Movimentação de {tipo} registrada com sucesso para o produto {produto.nome}!', 'success')
            return {'message': f'Movimentação de {tipo} registrada com sucesso.'}, 200
        else:
            flash('Produto não encontrado!', 'danger')
            return {'message': 'Erro: Produto não encontrado.'}, 400

    except Exception as e:
        flash(f'Erro ao registrar movimentação: {str(e)}', 'danger')
        db.session.rollback()
        return {'message': f'Erro ao registrar movimentação: {str(e)}'}, 500
