from flask import Blueprint, render_template
from models import Categoria, db
from encaminhar_contato import enviar_email  # Importe sua função de envio de e-mail
from keys import senha_, email_

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    categorias = Categoria.query.all()

    for categoria in categorias:
        # Atualiza o campo quantidade_total com base no total calculado a partir dos produtos
        categoria.atualizar_quantidade_total()
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

    db.session.commit()  # Comita todas as alterações de uma vez

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
