from flask import Blueprint, jsonify
from models import Relatorio
from datetime import datetime
from collections import defaultdict
import statistics

graficos_bp = Blueprint('graficos_bp', __name__)

# Dicionário de valores esperados para cada tarefa
expected_values = {
    "Colagem de Filme (Normal)": {
        "tempo_por_m2": 1.5,  # minutos por m² esperado
        "consumo": {"Filme": 1.0, "Cola Una": 50}
    },
    "Corte de Isopor": {
        "tempo_por_m2": 2.0,
        "consumo": {}
    },
    "Pintura Eletrostática": {
        "tempo_por_m2": 2.5,
        "consumo": {"Pó para Pintura": 120}
    },
    "Colagem de Cola Mel": {
        "tempo_por_m2": 1.2,
        "consumo": {"Cola Mel": 30}
    }
}

@graficos_bp.route("/chart_data", methods=["GET"])
def chart_data():
    # Consultar todos os relatórios
    relatorios = Relatorio.query.all()

    # Dados individuais de cada relatório com indicadores reais e esperados
    tarefas_individuais = []
    for rel in relatorios:
        # Obtém os valores esperados para a tarefa, se houver; caso contrário, usa valores padrão
        exp = expected_values.get(rel.tarefa, {"tempo_por_m2": None, "consumo": {}})
        tarefas_individuais.append({
            "id": rel.id,
            "tarefa": rel.tarefa,
            "duracao": rel.calcular_duracao(),
            "tempo_por_m2": rel.tempo_por_m2(),
            "consumo_por_m2": rel.consumo_por_m2(),
            "criado_em": rel.criado_em.strftime("%Y-%m-%d"),
            "expected_tempo_por_m2": exp.get("tempo_por_m2"),
            "expected_consumo_por_m2": exp.get("consumo")
        })

    # Agregação semanal: agrupando por ano e número da semana ISO (para tempo por m²)
    semanal_data = defaultdict(list)
    for rel in relatorios:
        ano = rel.criado_em.year
        semana = rel.criado_em.isocalendar()[1]
        key = f"{ano}-W{semana}"
        if rel.tempo_por_m2() is not None:
            semanal_data[key].append(rel.tempo_por_m2())
    media_semanal = {key: statistics.mean(values) for key, values in semanal_data.items()}

    # Agregação mensal: agrupando por ano e mês (para tempo por m²)
    mensal_data = defaultdict(list)
    for rel in relatorios:
        key = rel.criado_em.strftime("%Y-%m")
        if rel.tempo_por_m2() is not None:
            mensal_data[key].append(rel.tempo_por_m2())
    media_mensal = {key: statistics.mean(values) for key, values in mensal_data.items()}

    return jsonify({
        "tarefas_individuais": tarefas_individuais,
        "media_semanal": media_semanal,
        "media_mensal": media_mensal
    })
