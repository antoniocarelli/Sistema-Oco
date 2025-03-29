from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging
import os

from app.core.database import get_db
from app.core.security.base import SecurityBase
from app.schemas.user import UserCreate, Token, UserInDBBase, ForgotPassword, ResetPassword, VerifyResetToken
from app.models.user import User
from app.services.auth import (
    authenticate_user,
    create_user,
    get_current_active_user,
    create_access_token,
    get_user_by_email,
    get_password_hash,
    generate_reset_token,
    verify_reset_token,
    clear_reset_token
)
from app.services.email import send_reset_password_email

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
security_base = SecurityBase()

@router.post("/register", response_model=UserInDBBase)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Registra um novo usuário.
    """
    logger.info(f"Tentativa de registro para email: {user_in.email}")
    
    user = get_user_by_email(db, user_in.email)
    if user:
        logger.warning(f"Email já registrado: {user_in.email}")
        raise HTTPException(
            status_code=400,
            detail="Email já registrado",
        )
    
    logger.info(f"Criando novo usuário: {user_in.email}")
    user = create_user(db, user_in)
    logger.info(f"Usuário criado com sucesso: {user_in.email}")
    return user

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Login para obter token de acesso.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo",
        )
    
    access_token_expires = timedelta(minutes=security_base.access_token_expire_minutes)
    return create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

@router.get("/me", response_model=UserInDBBase)
def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtém informações do usuário atual.
    """
    return current_user

@router.post("/forgot-password")
async def forgot_password(
    *,
    db: Session = Depends(get_db),
    forgot_password_in: ForgotPassword,
) -> Any:
    """
    Inicia o processo de recuperação de senha.
    """
    user = get_user_by_email(db, forgot_password_in.email)
    if not user:
        # Por segurança, não informamos se o email existe ou não
        return {
            "message": "Se o email existir, você receberá instruções para redefinir sua senha"
        }
    
    # Gera o token de reset
    reset_token = generate_reset_token(db, user)
    
    # Envia o e-mail com o link de reset
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:4200")
    email_sent = await send_reset_password_email(user.email, reset_token, frontend_url)
    
    if not email_sent:
        logger.error(f"Falha ao enviar e-mail de reset para {user.email}")
        # Não informamos o erro ao usuário por segurança
        return {
            "message": "Se o email existir, você receberá instruções para redefinir sua senha"
        }
    
    logger.info(f"E-mail de reset enviado com sucesso para {user.email}")
    return {
        "message": "Se o email existir, você receberá instruções para redefinir sua senha"
    }

@router.post("/reset-password")
def reset_password(
    *,
    db: Session = Depends(get_db),
    reset_password_in: ResetPassword,
) -> Any:
    """
    Redefine a senha do usuário usando o token de reset.
    """
    user = verify_reset_token(db, reset_password_in.token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Token inválido ou expirado",
        )
    
    # Atualiza a senha
    user.hashed_password = get_password_hash(reset_password_in.new_password)
    
    # Limpa o token após a senha ser alterada
    clear_reset_token(db, user)
    
    return {"message": "Senha atualizada com sucesso"}

@router.post("/verify-reset-token")
def verify_reset_token_endpoint(
    *,
    db: Session = Depends(get_db),
    token_data: VerifyResetToken,
) -> Any:
    """
    Verifica se um token de reset é válido.
    """
    user = verify_reset_token(db, token_data.token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Token inválido ou expirado",
        )
    
    return {"message": "Token válido"} 