from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status
from config.config import settings

class SecurityBase:
    """
    Classe base para gerenciar autenticação e segurança.
    Fornece métodos básicos para manipulação de tokens JWT e autenticação.
    """
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Cria um token JWT de acesso.
        
        Args:
            data: Dados a serem codificados no token
            expires_delta: Tempo de expiração do token
            
        Returns:
            str: Token JWT gerado
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica e decodifica um token JWT.
        
        Args:
            token: Token JWT a ser verificado
            
        Returns:
            Dict[str, Any]: Dados decodificados do token
            
        Raises:
            HTTPException: Se o token for inválido
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_user_from_token(self, token: str) -> str:
        """
        Extrai o usuário de um token JWT.
        
        Args:
            token: Token JWT
            
        Returns:
            str: Nome do usuário
            
        Raises:
            HTTPException: Se o token for inválido ou não contiver usuário
        """
        payload = self.verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token não contém usuário",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username

    def create_refresh_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Cria um token de atualização com tempo de expiração mais longo.
        
        Args:
            data: Dados a serem codificados no token
            expires_delta: Tempo de expiração do token
            
        Returns:
            str: Token de atualização gerado
        """
        if expires_delta is None:
            expires_delta = timedelta(days=7)  # Token de atualização expira em 7 dias
        return self.create_access_token(data, expires_delta)

    def verify_refresh_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica um token de atualização.
        
        Args:
            token: Token de atualização
            
        Returns:
            Dict[str, Any]: Dados decodificados do token
            
        Raises:
            HTTPException: Se o token for inválido
        """
        return self.verify_token(token) 