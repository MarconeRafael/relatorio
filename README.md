
# Relatórios Automáticos com OpenAI, Transcrição de Áudio e Gestão de Almoxarifado

Este projeto utiliza a API da OpenAI para transcrever áudios e gerar relatórios organizados automaticamente. 
Inclui uma interface web para upload de áudios, visualização de gráficos, geração de relatórios em PDF e gestão de almoxarifado.

## 📂 Estrutura do Diretório

```
relatorios/
├── app.py
├── config.py
├── main.py
├── transcrever_audio.py
├── gerar_pdf.py
├── eficiencia_material.py
├── eficiencia_tempo.py
├── graficos_material.py
├── graficos_tempo.py
├── inicio.py
├── fim.py
├── keys.py
├── LICENSE
├── README.md
├── models.py
├── static/
│   ├── recorder.js
│   └── style.css
├── data/
│   ├── audios/
│   ├── graficos/
│   └── relatorios/
├── routes/
│   ├── __init__.py
│   ├── produtos.py
│   ├── movimentacoes.py
│   ├── fornecedores.py
│   └── usuarios.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── graficos.html
│   ├── relatorios.html
│   └── forms/
├── venv/
└── __pycache__/
           # Documentação do projeto
```

## 🚀 Como Usar

### 1️⃣ **Configuração Inicial**
```bash
# Clonar repositório e instalar dependências
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

pip install -r requirements.txt  # Instalar Flask, OpenAI e outras dependências
```

### 2️⃣ **Configurar Chave da OpenAI**
Edite `keys.py` e insira sua chave:
```python
chave_openai = "sua-chave-aqui"
```

### 3️⃣ **Executar Aplicação Web**
```bash
python app.py
```
Acesse http://localhost:5000 no navegador para:
- Gravar/upload de áudio diretamente na interface
- Visualizar relatórios processados
- Acessar gráficos de eficiência
- Download de relatórios em PDF
- Gerenciar o almoxarifado (produtos, movimentações, fornecedores e usuários)

### 4️⃣ **Fluxo de Processamento**
1. Áudio é salvo em `data/audios/`
2. Transcrição via OpenAI é armazenada temporariamente
3. Relatório estruturado é gerado e salvo em `data/relatorios/`
4. Gráficos são atualizados em `data/graficos/`

### 5️⃣ **Geração de Relatórios (CLI)**
Para processamento manual via terminal:
```python
from transcrever_audio import transcrever_audio
from inicio import organiza

texto = transcrever_audio("data/audios/seu_audio.ogg")
relatorio = organiza(texto)
print(relatorio)
```

### 6️⃣ **Geração de Gráficos (CLI)**
```python
from graficos_material import gerar_graficos as graf_materiais
from graficos_tempo import gerar_graficos as graf_tempo

graf_materiais()
graf_tempo()
```

## 📊 Saída Esperada
- Relatórios diários em CSV: `data/relatorios/relatorio_YYYY-MM-DD.csv`
- Gráficos atualizados: 
  - `data/graficos/eficiencia_material.png`
  - `data/graficos/eficiencia_tempo.png`
- PDF consolidado: `data/relatorios/relatorio_eficiencia.pdf`

## 🌐 Recursos da Interface Web
- Gravação de áudio direto no navegador
- Upload de arquivos de áudio (formato OGG)
- Visualização de histórico de relatórios
- Dashboard interativo com métricas de eficiência
- Download de relatórios em formato PDF
- Controle e gestão de almoxarifado

## 📜 Licença
Distribuído sob licença Apache 2.0. Veja [LICENSE](LICENSE) para detalhes.
