from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_email_config() -> ConnectionConfig:
    """
    Obtém a configuração do e-mail a partir das variáveis de ambiente.
    """
    # Validação das variáveis de ambiente
    required_vars = [
        "MAIL_USERNAME",
        "MAIL_PASSWORD",
        "MAIL_FROM",
        "MAIL_SERVER"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Variáveis de ambiente faltando: {', '.join(missing_vars)}")
    
    return ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

# Configuração do FastMail
try:
    conf = get_email_config()
except ValueError as e:
    print(f"Erro na configuração de e-mail: {str(e)}")
    conf = None

async def send_reset_password_email(email: EmailStr, token: str, frontend_url: str) -> bool:
    """
    Envia um e-mail com o link para reset de senha.
    
    Args:
        email: Email do usuário
        token: Token de reset de senha
        frontend_url: URL base do frontend
        
    Returns:
        bool: True se o e-mail foi enviado com sucesso, False caso contrário
    """
    if not conf:
        print("Configuração de e-mail não disponível")
        return False
        
    try:
        reset_link = f"{frontend_url}/reset-password?token={token}"
        
        message = MessageSchema(
            subject="Recuperação de Senha",
            recipients=[email],
            body=f"""
            <html>
                <body>
                    <h2>Recuperação de Senha</h2>
                    <p>Olá,</p>
                    <p>Você solicitou a recuperação de senha da sua conta. Clique no link abaixo para redefinir sua senha:</p>
                    <p><a href="{reset_link}">Redefinir Senha</a></p>
                    <p>Se você não solicitou esta recuperação de senha, por favor ignore este e-mail.</p>
                    <p>Este link expira em 24 horas.</p>
                    <p>Atenciosamente,<br>Equipe do Sistema</p>
                </body>
            </html>
            """,
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)
        return True
        
    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")
        return False 