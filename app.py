from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import main  # Sua lógica de processamento existente
import transcrever_audio  # Função de transcrição de áudio
from models import db  # Instância do SQLAlchemy
from routes.produtos import produtos_bp
from routes.movimentacoes import movimentacoes_bp
from routes.usuarios import usuarios_bp
from flask_migrate import Migrate
from flask_login import LoginManager
from models import Usuario  # Para o user_loader
from routes.categoria import categoria_bp  # Importação do Blueprint de categorias
from routes.unidades import unidades_bp  # Importação do Blueprint de unidades

# Criação do aplicativo Flask
app = Flask(__name__)

# Configurações do aplicativo
app.config['SECRET_KEY'] = 'sua-chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///almoxarifado.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados e o Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Inicializa o LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'usuarios_bp.login'  # Use o endpoint correto do blueprint de usuários

@login_manager.user_loader
def load_user(user_id):
    # Usando db.session.get para evitar o aviso LegacyAPIWarning
    return db.session.get(Usuario, int(user_id))

# Configurações de diretórios
app.config['GRAPHIQUE_DIR'] = os.path.join(os.getcwd(), 'data', 'graficos')
app.config['RELATORIO_DIR'] = os.path.join(os.getcwd(), 'data', 'relatorios')
app.config['AUDIOS_DIR'] = os.path.join(os.getcwd(), 'data', 'audios')

# Registro dos blueprints do sistema de almoxarifado
app.register_blueprint(produtos_bp, url_prefix="/produtos")
app.register_blueprint(movimentacoes_bp, url_prefix="/movimentacoes")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(categoria_bp, url_prefix="/categorias")  # Registro do Blueprint de Categorias
app.register_blueprint(unidades_bp, url_prefix="/unidades")  # Registro do Blueprint de Unidades

# Rotas principais
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Endpoint para processar o áudio enviado pelo navegador
@app.route("/processar_audio", methods=["POST"])
def processar_audio():
    try:
        if "audio_data" not in request.files:
            return jsonify({"error": "Nenhum arquivo de áudio enviado."}), 400

        audio_file = request.files["audio_data"]
        temp_audio_path = os.path.join(app.config['AUDIOS_DIR'], audio_file.filename)
        os.makedirs(os.path.dirname(temp_audio_path), exist_ok=True)
        audio_file.save(temp_audio_path)

        transcricao = transcrever_audio.transcrever_audio(temp_audio_path)
        return jsonify({"transcricao": transcricao})
    except Exception as e:
        return jsonify({"error": f"Erro: {e}"}), 500

# Endpoint para o processamento ao clicar em "Concluir"
@app.route("/concluir", methods=["POST"])
def concluir():
    try:
        dados = request.get_json()
        texto_inicial = dados.get('texto_inicial')
        texto_final = dados.get('texto_final')
        if not texto_inicial or not texto_final:
            return jsonify({"success": False, "error": "Textos de início e fim são obrigatórios."}), 400

        main.processar_textos(texto_inicial, texto_final)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Tela de Relatórios
@app.route("/relatorios")
def relatorios():
    pdf_path = f"data/relatorios/relatorio_completo.pdf"
    relatorio_pdf = "relatorio_completo_2025-03-05.pdf"
    relatorio_eficiencia_csv = "relatorio_eficiencia_material.csv"
    relatorio_eficiencia_pdf = "relatorio_eficiencia.pdf"
    return render_template("relatorios.html", 
                           pdf_path=pdf_path,
                           relatorio_pdf=relatorio_pdf,
                           relatorio_eficiencia_csv=relatorio_eficiencia_csv,
                           relatorio_eficiencia_pdf=relatorio_eficiencia_pdf)

# Tela de Gráficos
@app.route("/graficos")
def graficos():
    return render_template("graficos.html")

# Rotas para servir arquivos estáticos de gráficos e relatórios
@app.route('/graficos/<path:filename>')
def serve_graphics(filename):
    return send_from_directory(app.config['GRAPHIQUE_DIR'], filename)

@app.route('/relatorios/<path:filename>')
def serve_report(filename):
    return send_from_directory(app.config['RELATORIO_DIR'], filename)

if __name__ == "__main__":
    app.run(debug=True)
