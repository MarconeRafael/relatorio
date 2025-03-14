from flask import Blueprint, render_template
from models import Categoria, db
from encaminhar_contato import enviar_email  # Função de envio de e-mail
from keys import senha_, email_

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    categorias = Categoria.query.all()

    for categoria in categorias:
        # Atualiza a quantidade total de produtos associados à categoria
        categoria.atualizar_quantidade_total()
        total_produtos = categoria.quantidade_total
        
        # Se a quantidade total for menor ou igual à quantidade mínima e ainda não foi notificada, enviar e-mail
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
            # Se a quantidade estiver acima do mínimo e a categoria estiver marcada como notificada, redefinir o flag
            if categoria.notificado:
                categoria.notificado = False

    # Persiste todas as alterações no banco de dados
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
