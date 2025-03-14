# Relatórios Automáticos com OpenAI, Transcrição de Áudio e Gestão de Almoxarifado

Este projeto utiliza a API da OpenAI para transcrever áudios e gerar relatórios automaticamente, além de oferecer uma interface web para upload de áudios, visualização de gráficos, geração de relatórios em PDF e gestão de almoxarifado.

---

## 📂 Estrutura do Diretório

A estrutura atual do projeto é a seguinte:

```
relatorio/
├── app.py
├── config.py
├── eficiencia_material.py  #Não está sendo usado
├── eficiencia_tempo.py     #Não está sendo usado
├── fim.py                  #Não está sendo usado
├── gerar_pdf.py            #Não está sendo usado
├── graficos_material.py    #Não está sendo usado
├── graficos_tempo.py       #Não está sendo usado
├── inicio.py               #Não está sendo usado
├── instance/
├── keys.py
├── LICENSE
├── main.py                 #Não está sendo usado
├── migrations/
├── models.py
├── README.md
├── requirements.txt
├── routes/
│   ├── dashboard.py
│   ├── graficos.py
│   ├── processar_formulario.py
│   ├── produtos.py
│   ├── unidades.py
│   └── usuarios.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── chart.js
│   ├── recorder.js
│   └── style.css
├── templates/
│   ├── base.html
│   ├── cadastro.html
│   ├── cadastrar_unidade.html
│   ├── dashboard.html
│   ├── editar_produto.html
│   ├── editar_unidade.html
│   ├── graficos.html
│   ├── graficos2.html      #Não está sendo usado
│   ├── gravar.html
│   ├── index.html
│   ├── login.html
│   ├── novo_produto.html
│   ├── listar_unidades.html
│   ├── produtos.html
│   ├── relatorios.html     #Não está sendo usado
│   └── tabela.html
├── data/                   #Não está sendo usado
│   ├── audios/            
│   ├── graficos/
│   └── relatorios/
└── venv/
```

---

## 🚀 Como Usar

### 1️⃣ Configuração Inicial

Clone o repositório e instale as dependências:

```
git clone <URL-do-repositório>
cd relatorio
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Configurar a Chave da OpenAI

Edite o arquivo `keys.py` e insira sua chave da OpenAI:

```
chave_openai = "sua-chave-aqui"
```

### 3️⃣ Gerenciamento de Banco de Dados com Flask-Migrate

1. Inicializar as migrações:
```
flask db init
```
2. Gerar uma nova migração:
```
flask db migrate -m "Atualiza modelos"
```
3. Aplicar a migração:
```
flask db upgrade
```

### 4️⃣ Executar a Aplicação Web

```
python app.py
ou
flask run
```
Acesse [http://localhost:5000](http://localhost:5000).

---

## 📊 Funcionalidades

- Transcrição de Áudio com OpenAI
- Geração de Relatórios em PDF
- Gestão de Almoxarifado
- Dashboard Interativo com Gráficos

---

## 💻 Uso via Interface Web

- Gravação e Upload de Áudio
- Visualização de Relatórios
- Dashboard com Gráficos Interativos

---

## 🛠 Atualizações

O arquivo `processar_formulario.py` redireciona para `/dashboard` após salvar os dados.



## 📜 Licença
Distribuído sob licença Apache 2.0. Veja [LICENSE](LICENSE) para detalhes.
