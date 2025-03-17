from flask import Blueprint, jsonify
from models import Relatorio
from collections import defaultdict
import statistics

graficos_bp = Blueprint('graficos_bp', __name__)

expected_values = {
    "Pintura": {
        "tempo_por_m2": 2.5,  # minutos por m² esperado para pintura
        "consumo": {
            "Pó para Pintura": {
                "expected_total": 120,  # a soma dos consumos dos tipos selecionados deve totalizar 120
                "variants": {
                    "Pó para Pintura branco": 120,
                    "Pó para Pintura preto fosco": 120,
                    "Pó para Pintura terracota": 60,
                    "Pó para Pintura preto brilhoso": 120,
                    "Pó para Pintura cinza": 120,
                    "Pó para Pintura amarelo": 120,
                    "Pó para Pintura vermelho": 120
                }
            }
        }
    },
    "Colagem de filme": {
        "tempo_por_m2": 1.5,
        "consumo": {
            "Filme": 1.0,
            "Estilete": 15,
            "Álcool": 5,
            "Cola": {
                "expected_max": 60,  # valor máximo entre as opções (Cola Una ou Cola Kisafix)
                "variants": {
                    "Cola Una": 60,
                    "Cola Kisafix": 60
                }
            }
        }
    },
    "Colagem de eps": {
        "tempo_por_m2": 1.2,
        "consumo": {
            "Cola Mel": 200,
            "EPS": 1000,
            "Aço": 1,
            "Luvas": 100
        }
    },
    "Acabamento": {
        "tempo_por_m2": 1.0,
        "consumo": {
            "EPS": 1000,
            "Estilete": 15
        }
    },
    "Envio": {
        "tempo_por_m2": 0,  # não se aplica o consumo por área nesta tarefa
        "consumo": {
            "Parafuso": {
                "expected_max": 1000,  # valor máximo entre as opções disponíveis
                "variants": {
                    "Parafuso autobrocante": 1000,
                    "Parafuso costura": 50,
                    "cuminheeira": 1
                }
            }
        }
    }
}

@graficos_bp.route("/chart_data", methods=["GET"])
def chart_data():
    # Consultar todos os relatórios
    relatorios = Relatorio.query.all()

    tarefas_individuais = []
    for rel in relatorios:
        # Obtém os valores esperados para a tarefa, se houver; caso contrário, usa valores padrão
        exp = expected_values.get(rel.tarefa, {"tempo_por_m2": None, "consumo": {}})
        
        # Calcular o tempo total real e o tempo total esperado para a tarefa
        actual_tempo_total = rel.calcular_duracao()
        expected_tempo_total = None
        if exp.get("tempo_por_m2") is not None and rel.metros_quadrados:
            expected_tempo_total = exp.get("tempo_por_m2") * rel.metros_quadrados
        
        # O consumo real é o total registrado em materiais_gastos
        actual_consumo_total = rel.materiais_gastos
        
        # Calcular o consumo total esperado: para cada material esperado, multiplique pelo número de metros quadrados
        expected_consumo_total = {}
        for material, valor in exp.get("consumo", {}).items():
            if rel.metros_quadrados:
                if isinstance(valor, dict):
                    # Se existir "expected_total", utiliza-o; caso contrário, tenta "expected_max"
                    if "expected_total" in valor:
                        numeric_val = valor["expected_total"]
                    elif "expected_max" in valor:
                        numeric_val = valor["expected_max"]
                    else:
                        numeric_val = 0
                else:
                    numeric_val = valor
                expected_consumo_total[material] = numeric_val * rel.metros_quadrados
        
        tarefas_individuais.append({
            "id": rel.id,
            "tarefa": rel.tarefa,
            "duracao": rel.calcular_duracao(),
            "tempo_por_m2": rel.tempo_por_m2(),
            "consumo_por_m2": rel.consumo_por_m2(),
            "metros_quadrados": rel.metros_quadrados,
            "actual_tempo_total": actual_tempo_total,
            "expected_tempo_total": expected_tempo_total,
            "actual_consumo_total": actual_consumo_total,
            "expected_consumo_total": expected_consumo_total,
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
