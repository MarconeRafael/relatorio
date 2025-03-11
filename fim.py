import openai
import csv
import os
import re
from keys import chave_openai
from transcrever_audio import transcrever_audio
from datetime import datetime

# Configuração da chave da API
openai.api_key = chave_openai  

# Criar diretório caso não exista
os.makedirs("data/relatorios", exist_ok=True)

# Nome do arquivo CSV com data atual
CSV_FILE = f"data/relatorios/relatorio.csv"

# Garante que o cabeçalho do CSV seja escrito apenas se o arquivo não existir
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Horário de Início", "Tarefa", "Nome do Cliente",
            "Horário de Fim", "Material Gasto", "Metros Quadrados"
        ])

def normalize(text):
    """
    Função de normalização para a comparação:
    - Remove espaços laterais
    - Converte para minúsculas
    - Remove pontos finais (somente para comparação)
    """
    return text.strip().lower().rstrip('.')

def organiza_fim(texto):
    """
    Utiliza o GPT para extrair informações sobre término da tarefa, materiais gastos,
    metros quadrados e horário de fim.
    O GPT deve retornar o texto no formato:
    "Tarefa de (tarefa), do cliente (nome do cliente), foi gasto (material gasto),
    foi feito (metros quadrados), terminou na hora (hora de término)"
    
    Essa versão tenta lidar com variações, como "Encerrando a tarefa" e "terminou" sem "na hora".
    """
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Leia o texto e extraia as seguintes informações no formato: "
                        "'Tarefa de (tarefa), do cliente (nome do cliente), foi gasto (material gasto), "
                        "foi feito (metros quadrados), terminou na hora (hora de término)'. "
                        "Considere diferentes formas de falar a hora, por exemplo: 9 e 39 = 9:39 = 9 horas e 39 minutos, etc. "
                        "Se alguma informação estiver faltando, diga: 'Faltando: (a, b, c...)'."
                    )
                },
                {"role": "user", "content": texto}
            ],
            max_tokens=150,
            temperature=0.5
        )
        
        resposta_texto = resposta["choices"][0]["message"]["content"].strip()

        # Regex atualizada para aceitar "Encerrando a tarefa" ou "Tarefa de" e "terminou" opcionalmente com "na hora"
        padrao = (
            r"(?i)^(?:encerrando a tarefa|tarefa de)\s*"
            r"(?P<tarefa>.*?)\s*do cliente\s*(?P<cliente>.*?)\s*,\s*"
            r"foi gasto\s*(?P<material>.*?)\s*,\s*"
            r"foi feito\s*(?P<metros>.*?)\s*,\s*"
            r"terminou(?:\s*na hora)?\s*(?P<fim>.*)$"
        )
        match = re.match(padrao, resposta_texto)
        
        dados = {
            "Tarefa": "",
            "Nome do Cliente": "",
            "Material Gasto": "",
            "Metros Quadrados": "",
            "Horário de Fim": ""
        }
        
        if match:
            dados["Tarefa"] = match.group("tarefa").strip()
            dados["Nome do Cliente"] = match.group("cliente").strip()
            dados["Material Gasto"] = match.group("material").strip()
            dados["Metros Quadrados"] = match.group("metros").strip()
            dados["Horário de Fim"] = match.group("fim").strip()
        else:
            # Se a regex não funcionar, tenta fallback usando split (pode falhar se não houver 5 partes)
            partes = [p.strip() for p in resposta_texto.split(",")]
            if len(partes) >= 5:
                dados["Tarefa"] = partes[0].replace("Tarefa de ", "").replace("Encerrando a tarefa ", "").strip()
                # Supondo que o "do cliente" esteja contido na mesma parte
                if "do cliente" in partes[0]:
                    tarefa, cliente = partes[0].split("do cliente", 1)
                    dados["Tarefa"] = tarefa.replace("Tarefa de ", "").replace("Encerrando a tarefa ", "").strip()
                    dados["Nome do Cliente"] = cliente.strip()
                else:
                    dados["Nome do Cliente"] = partes[1].replace("do cliente ", "").strip()
                dados["Material Gasto"] = partes[1].replace("foi gasto ", "").strip() if len(partes) > 1 else ""
                dados["Metros Quadrados"] = partes[2].replace("foi feito ", "").strip() if len(partes) > 2 else ""
                dados["Horário de Fim"] = partes[3].replace("terminou", "").replace("na hora", "").strip() if len(partes) > 3 else ""
            else:
                # Se não conseguir extrair, retorna o texto para conferência
                return resposta_texto

        # Validação dos campos extraídos (apenas imprime campos faltantes para debug)
        campos_faltantes = [campo for campo, valor in dados.items() if not valor or "Faltando:" in valor]
        if campos_faltantes:
            print(f"Campos faltantes ou incompletos: {', '.join(campos_faltantes)}")
        
        # Ajusta a formatação do horário de fim se necessário
        horario_fim = dados["Horário de Fim"]
        if horario_fim:
            # Se o horário for composto apenas de dígitos e tiver 2 caracteres, prefixa com "0h"
            if horario_fim.isdigit() and len(horario_fim) == 2:
                dados["Horário de Fim"] = f"0h{horario_fim}"
            else:
                dados["Horário de Fim"] = horario_fim.strip()

        # Atualiza o CSV apenas nas linhas correspondentes utilizando comparação estrita (com normalização temporária)
        linhas_atualizadas = []
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)  # Lê o cabeçalho
            linhas = list(reader)

        for linha in linhas:
            # Comparação exata após normalizar os textos (sem alterar os dados do CSV)
            if (
                normalize(dados["Nome do Cliente"]) == normalize(linha[2]) and
                normalize(dados["Tarefa"]) == normalize(linha[1]) and
                linha[3].strip() == "" and
                linha[4].strip() == "" and
                linha[5].strip() == ""
            ):
                linha[3] = dados["Horário de Fim"]        # Preenche Horário de Fim
                linha[4] = dados["Material Gasto"]          # Preenche Material Gasto
                linha[5] = dados["Metros Quadrados"]        # Preenche Metros Quadrados

            linhas_atualizadas.append(linha)

        # Reescreve o arquivo CSV atualizado
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)         # Escreve o cabeçalho
            writer.writerows(linhas_atualizadas)  # Escreve os dados atualizados

        return resposta_texto  # Retorna o texto formatado para conferência

    except openai.error.OpenAIError as e:
        return f"Erro na API OpenAI: {str(e)}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"
