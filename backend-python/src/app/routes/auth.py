from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.security.base import SecurityBase
from app.schemas.user import UserCreate, Token, UserInDBBase
from app.models.user import User
from app.services.auth import (
    authenticate_user,
    create_user,
    get_current_active_user,
    create_access_token,
    get_user_by_email
)

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