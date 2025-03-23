from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import logging

from app.core.security.base import SecurityBase
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, Token, TokenPayload

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
security_base = SecurityBase()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user: UserCreate) -> User:
    logger.info(f"Iniciando criação de usuário: {user.email}")
    hashed_password = get_password_hash(user.password)
    logger.debug("Senha hasheada com sucesso")
    
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    logger.debug("Objeto User criado")
    
    db.add(db_user)
    logger.debug("Usuário adicionado à sessão do banco")
    
    try:
        db.commit()
        logger.debug("Commit realizado com sucesso")
        db.refresh(db_user)
        logger.info(f"Usuário criado com sucesso: {user.email}")
        return db_user
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        db.rollback()
        raise

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security_base.verify_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> Token:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    access_token = security_base.create_access_token(to_encode)
    refresh_token = security_base.create_refresh_token(to_encode)
    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    ) 