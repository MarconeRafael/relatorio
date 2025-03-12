from flask import Blueprint, render_template
from models import Categoria

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    categorias = Categoria.query.all()
    categorias_com_produtos = [
        {
            "id": categoria.id,
            "nome": categoria.nome,
            "descricao": categoria.descricao or "Sem descrição",
            "total_produtos": categoria.contar_produtos()
        }
        for categoria in categorias
    ]

    return render_template("dashboard.html", categorias=categorias_com_produtos)
