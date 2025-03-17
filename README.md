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



Adicionando Categorias Pré-Definidas via Flask Shell
Este documento descreve o processo para inserir os registros de categorias na tabela categorias do banco de dados utilizando o Flask Shell. Essas categorias são definidas no dicionário CATEGORIAS_PREDEFINIDAS no arquivo models.py.

Pré-requisitos
Ambiente Virtual Ativado: Certifique-se de que o ambiente virtual do projeto está ativo.
Banco de Dados Configurado: Verifique se o banco de dados está corretamente configurado (por exemplo, utilizando SQLite ou outra URI definida em app.py).
Migrações Aplicadas: Caso utilize Flask-Migrate, confirme que as migrações foram executadas e a tabela categorias existe.
Passos para Inserir as Categorias
1. Abra o Flask Shell
Na raiz do projeto, execute o comando:

bash
Copiar
Editar
flask shell
Isso abrirá o shell interativo do Flask, onde você pode interagir com o seu aplicativo.

2. Importe os Modelos e a Instância do Banco
No shell, importe a classe Categoria, a instância db e o dicionário CATEGORIAS_PREDEFINIDAS:

python
Copiar
Editar
from models import Categoria, db, CATEGORIAS_PREDEFINIDAS
3. Adicione as Categorias ao Banco de Dados
Utilize uma list comprehension para iterar sobre o dicionário e inserir cada categoria. Digite o seguinte comando:

python
Copiar
Editar
[db.session.add(Categoria(nome=nome, quantidade_minima=quantidade)) for nome, quantidade in CATEGORIAS_PREDEFINIDAS.items()]
Este comando adiciona cada nova categoria à sessão do banco de dados.

4. Confirme a Inserção com Commit
Após adicionar as categorias à sessão, é necessário confirmar (commit) as mudanças:

python
Copiar
Editar
db.session.commit()
5. Verifique se as Categorias Foram Inseridas
Para confirmar que as categorias foram adicionadas, execute:

python
Copiar
Editar
categorias = Categoria.query.all()
print(categorias)
O resultado deverá mostrar uma lista com os objetos da classe Categoria, por exemplo:

php-template
Copiar
Editar
[<Categoria Filme branco>, <Categoria Filme amadeirado>, <Categoria Filme preto>, ... ]
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
- Geração de Relatórios de produção
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
