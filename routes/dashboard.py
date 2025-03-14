from flask import Blueprint, render_template
from models import Categoria, db, Relatorio
from encaminhar_contato import enviar_email  # Função de envio de e-mail
from keys import senha_, email_

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    # 1. Atualiza o estoque base de cada categoria com base nos produtos
    categorias = Categoria.query.all()
    for categoria in categorias:
        categoria.atualizar_quantidade_total()
    db.session.commit()

    # 2. Aplica os materiais gastos para reduzir o estoque calculado
    relatorios = Relatorio.query.all()
    for rel in relatorios:
        rel.aplicar_materiais_gastos()
    db.session.commit()

    # 3. Atualiza as notificações de estoque baixo
    categorias = Categoria.query.all()  # Reconsulta para refletir os valores atualizados
    for categoria in categorias:
        total_produtos = categoria.quantidade_total
        if total_produtos <= categoria.quantidade_minima:
            if not categoria.notificado:
                enviar_email(
                    email_para=email_,
                    nome=categoria.nome,
                    email_de="mbteste518@gmail.com",
                    senha=senha_,
                    corpo_email=f"<p>O estoque da categoria {categoria.nome} está acabando. Quantidade atual: {total_produtos} e quantidade mínima: {categoria.quantidade_minima}.</p>"
                )
                categoria.notificado = True
        else:
            if categoria.notificado:
                categoria.notificado = False

    db.session.commit()

    categorias_com_produtos = [
        {
            "id": categoria.id,
            "nome": categoria.nome,
            "quantidade_minima": categoria.quantidade_minima,
            "total_produtos": categoria.quantidade_total
        }
        for categoria in categorias
    ]

    return render_template("dashboard.html", categorias=categorias_com_produtos)
