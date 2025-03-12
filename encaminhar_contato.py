#@title ##❏ 1. **Disparar email apenas com mensagem**


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
import pandas as pd
#from google.colab import drive
#drive.mount('/content/drive')

# Configurações gerais
data_atual = str(date.today())

# Função para enviar e-mails
def enviar_email(email_para, nome, email_de, senha, corpo_email):

    # Preparar a mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = email_de
    mensagem['To'] = email_para
    mensagem['Subject'] = "- Estoque baixo de "+ nome 
    mensagem.attach(MIMEText(corpo_email, 'html'))

    # Adicionar o anexo, se existir


    # Configuração do servidor SMTP para Gmail
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()

    try:
        # Login no servidor SMTP usando a senha de app do Gmail
        servidor.login(email_de, senha)
        # Enviar a mensagem
        servidor.send_message(mensagem)
        print('Enviado com sucesso!')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Erro de autenticação: {e}')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
    finally:
        servidor.quit()

# Configuração inicial do Gmail e senha de app
#email_gmail = 'XXXXXXXXXXXXXXXXXXXXXXX'  # Seu email Gmail
#senha_app = 'XXXXXXXXXXXXXXXXXXXXX'  # Sua senha de app gerada


