from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security.base import SecurityBase
from typing import Dict, Any

class AuthService(SecurityBase):
    """
    Serviço de autenticação que implementa a lógica específica de autenticação.
    Herda da classe base SecurityBase para gerenciamento de tokens.
    """
    
    def __init__(self):
        super().__init__()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> Dict[str, Any]:
        """
        Autentica um usuário e retorna tokens de acesso e atualização.
        
        Args:
            form_data: Dados do formulário de login
            
        Returns:
            Dict[str, Any]: Tokens de acesso e atualização
            
        Raises:
            HTTPException: Se as credenciais forem inválidas
        """
        # Aqui você implementaria a verificação real do usuário
        # Este é apenas um exemplo
        if form_data.username != "teste" or form_data.password != "teste":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Cria os tokens
        access_token = self.create_access_token(data={"sub": form_data.username})
        refresh_token = self.create_refresh_token(data={"sub": form_data.username})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> str:
        """
        Obtém o usuário atual a partir do token.
        
        Args:
            token: Token JWT
            
        Returns:
            str: Nome do usuário
        """
        return self.get_user_from_token(token)

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Gera um novo token de acesso usando um token de atualização válido.
        
        Args:
            refresh_token: Token de atualização
            
        Returns:
            Dict[str, Any]: Novo token de acesso
            
        Raises:
            HTTPException: Se o token de atualização for inválido
        """
        payload = self.verify_refresh_token(refresh_token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de atualização inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        new_access_token = self.create_access_token(data={"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"} 